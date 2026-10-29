"""Чат-бот / ассистент на лендинге и в ЛК."""

from __future__ import annotations

import time

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class ChatbotError(Exception):
    """Шаг проверки чат-бота не прошёл."""


# Только явная подпись виджета. Голое «bot» ловит bottom/cookiebot.
_LAUNCHER_JS = r"""
const re = /ассистент|помощник|чат[-\s]?бот|задать вопрос|написать (нам|в чат)/i;
const skip = /войти|логин|cookie|соглас|покупател|поставщик/i;
const clsOk = /chat-?bot|chatbot|assistant|jivo|webim|helpdesk|support-widget/i;
function walk(root, acc) {
  if (!root || !root.querySelectorAll) return;
  root.querySelectorAll(
    'button, a, [role="button"], [class*="chat"], [id*="chat"], [class*="assistant"], [id*="assistant"], [class*="widget"], [data-testid*="chat"]'
  ).forEach((el) => {
    acc.push(el);
    if (el.shadowRoot) walk(el.shadowRoot, acc);
  });
}
const nodes = [];
walk(document, nodes);
const hit = nodes.find((el) => {
  const label = ((el.getAttribute('aria-label') || el.getAttribute('title') || el.innerText || el.textContent || '') + '').trim();
  if (skip.test(label)) return false;
  const cls = ((el.className || '') + ' ' + (el.id || '')).toString();
  if (re.test(label) || clsOk.test(cls)) {
    const r = el.getBoundingClientRect();
    return r.width > 8 && r.height > 8 && r.bottom > 0;
  }
  return false;
});
return hit || null;
"""

_PANEL_JS = r"""
const sels = [
  '[role="dialog"]',
  '[class*="chat-window"]',
  '[class*="ChatWindow"]',
  '[class*="chat-panel"]',
  '[class*="ChatPanel"]',
  '[class*="assistant-window"]',
  '[data-testid*="chat"]',
];
const nodes = [];
sels.forEach((s) => document.querySelectorAll(s).forEach((el) => nodes.push(el)));
return nodes.find((el) => {
  const r = el.getBoundingClientRect();
  return r.width > 160 && r.height > 120 && r.bottom > 0;
}) || null;
"""

_PANEL_TEXT_JS = r"""
const root = document.body;
return (root && (root.innerText || root.textContent) || '').slice(0, 4000);
"""

_NAV_RE = ("назад", "вернуться в начало", "в начало", "на главную")
_CLOSE_RE = ("закрыть", "свернуть", "close")
_SKIP_TOPIC = _NAV_RE + _CLOSE_RE + (
    "отправить",
    "send",
    "прикрепить",
    "войти",
    "логин",
    "cookie",
    "соглас",
    "покупател",
    "поставщик",
    "поддержка бизнеса",
    "маркетплейс",
    "отраслевые",
    "другие сервисы",
    "получить id",
    "получить идентификатор",
    "добавить",
    "нерезидент",
    "филиал",
    "отправить запрос",
    "подробнее",
    "узнать больше",
)


class ChatbotWidget:
    def __init__(self, driver: WebDriver, *, timeout: int = 20):
        self.driver = driver
        self.timeout = timeout
        self._opened = False
        self._answer_seen = False
        self._last_topic = ""
        self._text_before_question = ""
        self._topics_before_open = 0

    def _switch_default(self) -> None:
        try:
            self.driver.switch_to.default_content()
        except WebDriverException:
            pass

    def _iframes(self):
        try:
            return list(self.driver.find_elements(By.TAG_NAME, "iframe"))
        except WebDriverException:
            return []

    def _click(self, element) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView({block:'end'});", element)
        try:
            element.click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", element)

    def _first_context(self, fn):
        """fn() на странице и в iframe; клик делать внутри fn, пока frame открыт."""
        self._switch_default()
        result = fn()
        if result:
            return result
        for frame in self._iframes():
            try:
                self.driver.switch_to.frame(frame)
                result = fn()
                if result:
                    return result
            except WebDriverException:
                continue
            finally:
                self._switch_default()
        return None

    def _current_text(self) -> str:
        try:
            return self.driver.execute_script(_PANEL_TEXT_JS) or ""
        except WebDriverException:
            return ""

    def _all_text(self) -> str:
        chunks: list[str] = []
        self._switch_default()
        chunks.append(self._current_text())
        for frame in self._iframes():
            try:
                self.driver.switch_to.frame(frame)
                chunks.append(self._current_text())
            except WebDriverException:
                continue
            finally:
                self._switch_default()
        return "\n".join(chunks)

    def _visible_buttons(self) -> list[tuple[object, str]]:
        found: list[tuple[object, str]] = []
        try:
            buttons = self.driver.find_elements(
                By.CSS_SELECTOR,
                "button, [role='button'], a, [class*='chip'], [class*='topic'], [class*='suggest']",
            )
        except WebDriverException:
            return found
        seen: set[str] = set()
        for btn in buttons:
            try:
                if not btn.is_displayed():
                    continue
            except WebDriverException:
                continue
            text = " ".join((btn.text or btn.get_attribute("aria-label") or "").split())[:80]
            key = text.lower()
            if not key or key in seen:
                continue
            seen.add(key)
            found.append((btn, text))
        return found

    def _is_noise(self, text: str) -> bool:
        key = text.lower()
        return any(s in key for s in _SKIP_TOPIC) or len(text) > 80 or len(text) < 2

    def _topic_candidates(self) -> list[tuple[object, str]]:
        return [(btn, text) for btn, text in self._visible_buttons() if not self._is_noise(text)]

    def _panel_present(self) -> bool:
        def look():
            try:
                return bool(self.driver.execute_script(_PANEL_JS))
            except WebDriverException:
                return False

        return bool(self._first_context(look))

    def _collect_topics(self) -> list[tuple[object, str]]:
        topics: list[tuple[object, str]] = []

        def grab():
            topics.extend(self._topic_candidates())
            return False

        self._first_context(grab)
        uniq: list[tuple[object, str]] = []
        seen: set[str] = set()
        for btn, text in topics:
            if text.lower() in seen:
                continue
            seen.add(text.lower())
            uniq.append((btn, text))
        return uniq

    def _launcher_visible(self) -> bool:
        def look():
            try:
                return self.driver.execute_script(_LAUNCHER_JS) is not None
            except WebDriverException:
                return False

        return bool(self._first_context(look))

    def step_icon_visible(self, context: str) -> None:
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            if self._launcher_visible():
                return
            time.sleep(0.3)
        raise ChatbotError(f"{context}: иконка чат-бота не отображается")

    def step_icon_clickable(self, context: str) -> None:
        def try_click():
            el = self.driver.execute_script(_LAUNCHER_JS)
            if el is None:
                return None
            try:
                if el.get_attribute("disabled"):
                    raise ChatbotError(f"{context}: иконка чат-бота некликабельна (disabled)")
            except ChatbotError:
                raise
            except WebDriverException:
                pass
            try:
                self._click(el)
            except WebDriverException as exc:
                raise ChatbotError(
                    f"{context}: не удалось кликнуть по иконке чат-бота: {exc}"
                ) from exc
            return True

        self._topics_before_open = len(self._collect_topics())
        try:
            ok = self._first_context(try_click)
        except ChatbotError:
            raise
        if not ok:
            raise ChatbotError(f"{context}: иконка чат-бота пропала до клика")
        time.sleep(1.2)
        self._opened = True

    def step_topics_displayed(self, context: str) -> None:
        deadline = time.time() + self.timeout
        topics: list[tuple[object, str]] = []
        while time.time() < deadline:
            topics = self._collect_topics()
            opened_panel = self._panel_present()
            appeared = len(topics) > self._topics_before_open
            if topics and (opened_panel or appeared):
                return
            time.sleep(0.4)
        preview = self._all_text()[:240]
        raise ChatbotError(
            f"{context}: после открытия чата темы не отображаются. Текст: {preview!r}"
        )

    def step_select_question(self, context: str) -> None:
        chosen: dict[str, str] = {}

        def try_click():
            topics = self._topic_candidates()
            if not topics:
                return None
            self._text_before_question = self._all_text()
            btn, text = topics[0]
            try:
                self._click(btn)
            except WebDriverException as exc:
                raise ChatbotError(
                    f"{context}: не удалось кликнуть тему {text!r}: {exc}"
                ) from exc
            chosen["topic"] = text
            time.sleep(1.2)
            nested = [item for item in self._topic_candidates() if item[1].lower() != text.lower()]
            if nested:
                nbtn, ntext = nested[0]
                try:
                    self._click(nbtn)
                except WebDriverException as exc:
                    raise ChatbotError(
                        f"{context}: не удалось выбрать вопрос {ntext!r}: {exc}"
                    ) from exc
                chosen["topic"] = ntext
                time.sleep(1.2)
            return True

        try:
            ok = self._first_context(try_click)
        except ChatbotError:
            raise
        if not ok:
            raise ChatbotError(f"{context}: нет темы, на которую можно кликнуть")
        self._last_topic = chosen.get("topic", "")

    def step_answers_received(self, context: str) -> None:
        deadline = time.time() + self.timeout
        before = self._text_before_question or ""
        after = ""
        while time.time() < deadline:
            after = self._all_text()
            grew = len(after.strip()) > max(40, len(before.strip()) + 10)
            has_topic = bool(self._last_topic) and self._last_topic in after
            if grew or (has_topic and len(after.strip()) > 40):
                self._answer_seen = True
                return
            time.sleep(0.4)
        raise ChatbotError(
            f"{context}: ответ на вопрос не получен (тема {self._last_topic!r}). "
            f"Текст: {after[:240]!r}"
        )

    def step_back_or_start(self, context: str) -> None:
        def try_nav():
            for btn, text in self._visible_buttons():
                key = text.lower()
                if any(n in key for n in _NAV_RE):
                    self._click(btn)
                    return text
            return None

        label = self._first_context(try_nav)
        if not label:
            raise ChatbotError(
                f"{context}: нет кнопки «Назад» или «Вернуться в начало»"
            )
        time.sleep(0.8)

    def step_close_window(self, context: str) -> None:
        def try_close():
            for btn, text in self._visible_buttons():
                key = text.lower()
                if any(n in key for n in _CLOSE_RE) or text in {"×", "✕", "x", "X"}:
                    self._click(btn)
                    return True
            return None

        closed = self._first_context(try_close)
        if not closed:
            self._switch_default()
            try:
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            except WebDriverException as exc:
                raise ChatbotError(
                    f"{context}: нет кнопки закрытия окна чат-бота и Escape не сработал: {exc}"
                ) from exc
        time.sleep(0.8)
        if self._panel_present():
            raise ChatbotError(
                f"{context}: после закрытия окно чат-бота всё ещё открыто"
            )
        self._opened = False

    def assert_interactive(self, *, context: str) -> None:
        """Полный сценарий: иконка → темы → вопрос → ответ → назад/начало → закрытие."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            pass
        self.step_icon_visible(context)
        self.step_icon_clickable(context)
        self.step_topics_displayed(context)
        self.step_select_question(context)
        self.step_answers_received(context)
        self.step_back_or_start(context)
        self.step_close_window(context)

    def close(self) -> None:
        if not self._opened:
            return
        try:
            self.step_close_window("чат-бот")
        except ChatbotError:
            self._switch_default()
            try:
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            except WebDriverException:
                pass
            self._opened = False

    def health_steps(self, prefix: str):
        """Шаги для health/Grafana — по одному CheckResult."""
        ctx = "Лендинг" if prefix.startswith("landing") else "ЛК"
        return [
            (f"{prefix}_icon", lambda: self._icon_both(ctx)),
            (f"{prefix}_topics", lambda: self.step_topics_displayed(ctx)),
            (f"{prefix}_question", lambda: self.step_select_question(ctx)),
            (f"{prefix}_answer", lambda: self.step_answers_received(ctx)),
            (f"{prefix}_nav", lambda: self.step_back_or_start(ctx)),
            (f"{prefix}_close", lambda: self.step_close_window(ctx)),
        ]

    def _icon_both(self, context: str) -> None:
        self.step_icon_visible(context)
        self.step_icon_clickable(context)
