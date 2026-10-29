"""Страница Минцифр / российские сертификаты на лендинге."""

from __future__ import annotations

import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.widget_urls import (
    is_blank_target,
    is_certs_href,
    is_certs_target,
    is_login_target,
    is_yandex_browser_href,
    mentions_yandex_browser,
    normalize_page_text,
)


class MincifryError(Exception):
    """Шаг проверки Минцифр не прошёл."""


BANNER_SNIPPETS = (
    "Установите российские сертификаты",
    "не терять доступ к сервисам",
    "российские сертификаты",
)
FAQ_SNIPPETS = (
    "ответы на частые вопросы",
    "частые вопросы",
    "часто задаваемые вопросы",
    "часто задаваемый вопрос",
    "вопросы и ответы",
    "faq",
)
_FAQ_EXPAND_SKIP = (
    "установить сертификаты",
    "скачать браузер",
    "скачать яндекс",
    "войти",
    "получить id",
    "регистрац",
)


class MincifryPage:
    def __init__(self, driver: WebDriver, *, timeout: int = 20):
        self.driver = driver
        self.timeout = timeout

    def _body_text(self) -> str:
        try:
            return (
                self.driver.execute_script(
                    "return (document.body && (document.body.innerText || document.body.textContent) || '');"
                )
                or ""
            )
        except WebDriverException:
            return self.driver.page_source or ""

    def _page_text(self) -> str:
        chunks = [self._body_text()]
        try:
            frames = list(self.driver.find_elements(By.TAG_NAME, "iframe"))
        except WebDriverException:
            frames = []
        for frame in frames[:8]:
            try:
                self.driver.switch_to.frame(frame)
                chunks.append(self._body_text())
            except WebDriverException:
                continue
            finally:
                try:
                    self.driver.switch_to.default_content()
                except WebDriverException:
                    pass
        return "\n".join(chunks)

    def _has_yandex_browser(self) -> bool:
        if mentions_yandex_browser(self._page_text()):
            return True
        try:
            hrefs = [
                el.get_attribute("href") or ""
                for el in self.driver.find_elements(By.CSS_SELECTOR, "a[href]")
            ]
        except WebDriverException:
            hrefs = []
        if any(is_yandex_browser_href(href) for href in hrefs):
            return True
        source = (self.driver.page_source or "").lower()
        return any(
            token in source
            for token in ("browser.yandex", "yandex.ru/download", "ya.ru/browser")
        )

    def _debug_where(self) -> str:
        url = self.driver.current_url or ""
        snippet = normalize_page_text(self._page_text())[:220]
        return f" url={url!r} текст={snippet!r}"

    def _visible_by_texts(self, snippets: tuple[str, ...]):
        """Самый короткий видимый узел с текстом — не html/body/main, иначе клик попадёт в «Войти»."""
        best = None
        best_len = 10**9
        best_area = 10**9
        skip_tags = {"html", "body", "script", "style", "head", "main", "header", "footer", "nav"}
        for snippet in snippets:
            xpath = f"//*[contains(normalize-space(.), '{snippet}')]"
            try:
                matches = self.driver.find_elements(By.XPATH, xpath)
            except WebDriverException:
                continue
            for el in matches:
                try:
                    tag = (el.tag_name or "").lower()
                    if tag in skip_tags:
                        continue
                    if not el.is_displayed():
                        continue
                    text = " ".join((el.text or "").split())
                    if not text or len(text) > 500:
                        continue
                    try:
                        size = el.size or {}
                        area = int(size.get("width") or 0) * int(size.get("height") or 0)
                    except WebDriverException:
                        area = 10**9
                    if len(text) < best_len or (len(text) == best_len and area < best_area):
                        best = el
                        best_len = len(text)
                        best_area = area
                except WebDriverException:
                    continue
        return best

    def _wait_banner(self):
        deadline = time.time() + self.timeout
        last = None
        scrolled = 0
        while time.time() < deadline:
            last = self._visible_by_texts(BANNER_SNIPPETS)
            if last is not None:
                try:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});", last
                    )
                except WebDriverException:
                    pass
                return last
            if scrolled < 8:
                try:
                    self.driver.execute_script("window.scrollBy(0, 500);")
                except WebDriverException:
                    pass
                scrolled += 1
            time.sleep(0.4)
        return last

    def _href_of(self, element) -> str:
        try:
            return (element.get_attribute("href") or "").strip()
        except WebDriverException:
            return ""

    def _own_label(self, element) -> str:
        try:
            return " ".join(
                (
                    element.get_attribute("aria-label")
                    or element.get_attribute("title")
                    or element.text
                    or ""
                ).split()
            )[:120]
        except WebDriverException:
            return ""

    def _is_usable_click_target(self, element) -> bool:
        if element is None:
            return False
        href = self._href_of(element)
        if href and (is_blank_target(href) or is_login_target(href)):
            return False
        text = self._own_label(element).lower()
        if is_login_target(text) or any(
            s in text for s in ("войти", "регистрац", "получить id", "получить идентификатор")
        ):
            return False
        return True

    def _certs_link(self):
        try:
            links = self.driver.find_elements(By.CSS_SELECTOR, "a[href]")
        except WebDriverException:
            return None
        for el in links:
            try:
                if not el.is_displayed():
                    continue
            except WebDriverException:
                continue
            href = self._href_of(el)
            text = self._own_label(el)
            if is_certs_href(href) or (
                len(text) <= 80 and is_certs_target(href, text) and self._is_usable_click_target(el)
            ):
                if self._is_usable_click_target(el):
                    return el
        return None

    def _auth_ancestor_href(self, node) -> str:
        try:
            found = node.find_element(By.XPATH, "./ancestor-or-self::a[1]")
            href = self._href_of(found)
            if is_login_target(href):
                return href
        except WebDriverException:
            pass
        return ""

    def _nearby_cta(self, node):
        """Только CTA про сертификаты в том же блоке, не «Войти»/регистрация."""
        container = node
        for _ in range(6):
            try:
                text_len = len(" ".join((container.text or "").split()))
            except WebDriverException:
                break
            if text_len > 420:
                break
            try:
                candidates = container.find_elements(
                    By.CSS_SELECTOR, "a[href], button, [role='button'], [role='link']"
                )
            except WebDriverException:
                candidates = []
            usable = []
            for el in candidates:
                try:
                    if not el.is_displayed() or not self._is_usable_click_target(el):
                        continue
                except WebDriverException:
                    continue
                href = self._href_of(el)
                label = self._own_label(el)
                if is_certs_href(href):
                    return el
                if is_certs_target(href, label):
                    usable.append(el)
            if usable:
                return usable[0]
            try:
                container = container.find_element(By.XPATH, "..")
            except WebDriverException:
                break
        return None

    def _pointer_parent(self, node):
        """Карточка баннера (cursor:pointer / role=button), не ссылка входа."""
        if node is None:
            return None
        try:
            found = self.driver.execute_script(
                """
                const el = arguments[0];
                const bad = /openid-connect|self-authentication|\\/registration|\\/login|keycloak/i;
                let n = el;
                for (let i = 0; i < 10 && n && n !== document.body && n !== document.documentElement; i++) {
                  const tag = (n.tagName || '').toLowerCase();
                  const href = (n.href || (n.getAttribute && n.getAttribute('href')) || '');
                  if (bad.test(String(href))) {
                    n = n.parentElement;
                    continue;
                  }
                  const role = (n.getAttribute && n.getAttribute('role')) || '';
                  let cursor = '';
                  try { cursor = getComputedStyle(n).cursor; } catch (e) {}
                  const textLen = ((n.innerText || n.textContent || '') + '').trim().length;
                  if (textLen > 700) break;
                  if (tag === 'a' || tag === 'button' || role === 'button' || role === 'link'
                      || n.onclick || cursor === 'pointer') {
                    return n;
                  }
                  n = n.parentElement;
                }
                return el;
                """,
                node,
            )
        except WebDriverException:
            found = node
        if found is None:
            return node
        if self._auth_ancestor_href(found):
            return None
        return found

    def _visible_links_dump(self) -> str:
        rows: list[str] = []
        try:
            links = self.driver.find_elements(By.CSS_SELECTOR, "a[href]")
        except WebDriverException:
            return ""
        for el in links:
            try:
                if not el.is_displayed():
                    continue
            except WebDriverException:
                continue
            href = self._href_of(el)
            label = self._own_label(el)[:70]
            if not href:
                continue
            rows.append(f"{label!r} -> {href}")
            if len(rows) >= 12:
                break
        return " | ".join(rows)

    def _clickable_from(self, node):
        """Карточка сертификатов: ссылка / JS-div / сам баннер — не вход и не регистрация."""
        if node is None:
            return None
        for xpath in ("./ancestor-or-self::a[1]", "./ancestor-or-self::button[1]"):
            try:
                found = node.find_element(By.XPATH, xpath)
            except WebDriverException:
                continue
            href = self._href_of(found)
            if is_login_target(href) or self._auth_ancestor_href(found):
                continue
            if is_certs_href(href) or is_certs_target(href, self._own_label(found)):
                return found
        card = self._pointer_parent(node)
        if card is not None and not self._auth_ancestor_href(card):
            return card
        cta = self._nearby_cta(node)
        if cta is not None and not self._auth_ancestor_href(cta):
            return cta
        if not self._auth_ancestor_href(node):
            return node
        return None

    def _click(self, element) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        try:
            element.click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", element)

    def step_banner_visible(self) -> None:
        banner = self._wait_banner()
        if banner is None:
            raise MincifryError(
                "На лендинге не отображается блок «Установите российские сертификаты, "
                "чтобы не терять доступ к сервисам»"
            )

    def step_banner_clickable(self) -> None:
        banner = self._wait_banner()
        if banner is None:
            raise MincifryError("Блок Минцифр пропал до клика")
        target = self._certs_link() or self._clickable_from(banner)
        trapped = self._auth_ancestor_href(target) if target is not None else self._auth_ancestor_href(banner)
        if target is None or trapped:
            raise MincifryError(
                "Блок сертификатов вложен в ссылку входа/регистрации или некликабелен, "
                f"отдельной карточки нет: {(trapped or '')!r}. "
                f"Видимые ссылки: {self._visible_links_dump() or 'нет'}"
            )
        href = self._href_of(target)
        print(
            f"  mincifry click tag={(target.tag_name or '').lower()!r} "
            f"href={href!r} label={self._own_label(target)!r}",
            flush=True,
        )
        if href and is_login_target(href):
            raise MincifryError(
                f"Клик Минцифр указывает на вход/регистрацию, а не на сертификаты: {href!r}"
            )

        before = set(self.driver.window_handles)
        before_url = self.driver.current_url
        try:
            self._click(target)
        except WebDriverException as exc:
            raise MincifryError(f"Не удалось кликнуть блок Минцифр: {exc}") from exc

        deadline = time.time() + self.timeout
        while time.time() < deadline:
            extra = [h for h in self.driver.window_handles if h not in before]
            if extra:
                self.driver.switch_to.window(extra[-1])
            url = (self.driver.current_url or "").strip()
            if is_login_target(url):
                raise MincifryError(
                    "Клик по блоку Минцифр открыл вход или регистрацию, "
                    f"а не сертификаты:{self._debug_where()}"
                )
            text = normalize_page_text(self._page_text())
            opened = bool(extra) or url != before_url or self._has_yandex_browser()
            loaded = (not is_blank_target(url)) and (len(text) > 20 or self._has_yandex_browser())
            if opened and loaded:
                return
            if opened and is_blank_target(url):
                time.sleep(0.4)
                continue
            time.sleep(0.4)
        url = (self.driver.current_url or "").strip()
        if is_login_target(url):
            raise MincifryError(
                "Клик по блоку Минцифр открыл вход или регистрацию, "
                f"а не сертификаты:{self._debug_where()}"
            )
        if is_blank_target(url):
            raise MincifryError(f"После клика открылся пустой URL:{self._debug_where()}")
        raise MincifryError(f"Клик по блоку Минцифр не открыл новую страницу:{self._debug_where()}")

    def step_yandex_browser_section(self) -> None:
        deadline = time.time() + max(self.timeout, 30)
        while time.time() < deadline:
            if self._has_yandex_browser():
                return
            time.sleep(0.4)
        raise MincifryError(
            "На странице нет указания по установке Яндекс Браузера:"
            f"{self._debug_where()}"
        )

    def step_certs_section(self) -> None:
        text = normalize_page_text(self._page_text())
        has_cert = "сертификат" in text
        has_mincifry = any(s in text for s in ("минцифр", "мин цифр", "нуц"))
        if has_cert and has_mincifry:
            return
        if has_cert and self._visible_by_texts(("Минцифр", "Минцифры", "НУЦ")):
            return
        raise MincifryError(
            "На странице нет блока установки сертификатов Минцифры:"
            f"{self._debug_where()}"
        )

    def _find_by_inner_text(self, needles: tuple[str, ...]):
        """Видимый узел по innerText без учёта регистра (кириллица в XPath translate ломается)."""
        lowered = [n.lower() for n in needles if n]
        if not lowered:
            return None
        try:
            return self.driver.execute_script(
                """
                const needles = arguments[0];
                const skip = new Set(
                  ['html','body','script','style','head','main','header','footer','nav']
                );
                let best = null;
                let bestLen = 1e9;
                let bestArea = 1e9;
                const nodes = document.querySelectorAll('*');
                for (const el of nodes) {
                  const tag = (el.tagName || '').toLowerCase();
                  if (skip.has(tag)) continue;
                  let text = '';
                  try { text = String(el.innerText || el.textContent || ''); } catch (e) { continue; }
                  text = text.replace(/\\s+/g, ' ').trim().toLowerCase();
                  if (!text || text.length > 240) continue;
                  if (!needles.some((n) => text.includes(n))) continue;
                  let style;
                  try { style = window.getComputedStyle(el); } catch (e) { continue; }
                  if (!style || style.display === 'none' || style.visibility === 'hidden') continue;
                  if (Number(style.opacity) === 0) continue;
                  const rect = el.getBoundingClientRect();
                  if (rect.width < 2 || rect.height < 2) continue;
                  const area = rect.width * rect.height;
                  if (text.length < bestLen || (text.length === bestLen && area < bestArea)) {
                    best = el;
                    bestLen = text.length;
                    bestArea = area;
                  }
                }
                return best;
                """,
                lowered,
            )
        except WebDriverException:
            return None

    def _faq_root(self):
        node = self._find_by_inner_text(FAQ_SNIPPETS)
        if node is None:
            node = self._visible_by_texts(
                (
                    "Ответы на частые вопросы",
                    "Частые вопросы",
                    "Часто задаваемые вопросы",
                    "Вопросы и ответы",
                    "FAQ",
                )
            )
        if node is None:
            return None
        try:
            found = self.driver.execute_script(
                """
                const el = arguments[0];
                const wrapRe = /questions|faq|accordion|collapseGroup|collapse-group/i;
                const titleRe = /questions__title|faq__title|accordion__title/i;
                let n = el;
                for (let i = 0; i < 12 && n && n !== document.body
                     && n !== document.documentElement; i++) {
                  const raw = (n.className && n.className.baseVal != null)
                    ? n.className.baseVal
                    : (n.className || (n.getAttribute && n.getAttribute('class')) || '');
                  const cls = String(raw);
                  if (wrapRe.test(cls) && !titleRe.test(cls)) return n;
                  n = n.parentElement;
                }
                return el.closest('[class*="questions"]')
                  || el.closest('[class*="faq"]')
                  || el.closest('[class*="accordion"]')
                  || el.closest('section')
                  || el.parentElement
                  || el;
                """,
                node,
            )
        except WebDriverException:
            found = node
        root = found or node
        if root is None:
            return None
        try:
            has_widget = self.driver.execute_script(
                """
                const el = arguments[0];
                return !!(el && el.querySelector
                  && el.querySelector(
                    '.Collapse-Label, [class*="Collapse-Label"], details, summary, [aria-expanded]'
                  ));
                """,
                root,
            )
        except WebDriverException:
            has_widget = True
        if not has_widget:
            try:
                parent = root.find_element(By.XPATH, "..")
                root = parent
            except WebDriverException:
                pass
        return root

    def step_faq_visible(self) -> None:
        text = normalize_page_text(self._page_text())
        if self._faq_root() is None and not any(s in text for s in FAQ_SNIPPETS):
            raise MincifryError(
                "На странице Минцифр не отображается блок с частыми вопросами:"
                f"{self._debug_where()}"
            )

    def _collapse_body_height(self, element) -> float:
        try:
            height = self.driver.execute_script(
                """
                const el = arguments[0];
                if (!el) return 0;
                const item = el.closest('.Collapse') || el.parentElement;
                let body = null;
                if (item) {
                  body = item.querySelector('.Collapse-Body')
                    || item.querySelector('[class*="Collapse-Body"]');
                }
                if (!body) return 0;
                return body.getBoundingClientRect().height || 0;
                """,
                element,
            )
            return float(height or 0)
        except (WebDriverException, TypeError, ValueError):
            return 0.0

    def _is_expanded(self, element) -> bool:
        aria = (element.get_attribute("aria-expanded") or "").lower()
        if aria == "true":
            return True
        try:
            details = element.find_element(By.XPATH, "./ancestor-or-self::details[1]")
            if details.get_attribute("open") is not None:
                return True
        except WebDriverException:
            pass
        return self._collapse_body_height(element) > 20

    def _faq_expand_targets(self, root):
        """Только FAQ-контролы внутри корня: Consta Collapse, затем details/aria."""
        groups = (
            ".Collapse-Label, [class*='Collapse-Label']",
            "details, summary, [aria-expanded]",
        )
        for css in groups:
            found = []
            try:
                candidates = root.find_elements(By.CSS_SELECTOR, css)
            except WebDriverException:
                candidates = []
            for el in candidates:
                try:
                    if not el.is_displayed():
                        continue
                except WebDriverException:
                    continue
                label = self._own_label(el).lower()
                if any(s in label for s in _FAQ_EXPAND_SKIP):
                    continue
                if not self._is_usable_click_target(el):
                    continue
                found.append(el)
            if found:
                return found
        return []

    def step_faq_expandable(self) -> None:
        root = self._faq_root()
        if root is None:
            raise MincifryError(
                "Блок частых вопросов не найден как контейнер, раскрывать нечего:"
                f"{self._debug_where()}"
            )
        clickable = self._faq_expand_targets(root)
        if not clickable:
            raise MincifryError("Блок частых вопросов есть, но его нельзя раскрыть")

        target = clickable[0]
        already = self._is_expanded(target)
        before_h = self._collapse_body_height(target)
        try:
            self._click(target)
        except WebDriverException as exc:
            raise MincifryError(f"Не удалось раскрыть частый вопрос: {exc}") from exc
        deadline = time.time() + 2.5
        while time.time() < deadline:
            if already or self._is_expanded(target):
                return
            after_h = self._collapse_body_height(target)
            if after_h > 20 or (before_h <= 20 and after_h > before_h + 8):
                return
            time.sleep(0.2)
        raise MincifryError("Клик по частому вопросу не раскрыл блок")

    def step_footer_visible(self) -> None:
        selectors = (
            "footer",
            "[class*='footer']",
            "[id*='footer']",
            "[data-testid='md-footer']",
        )
        for css in selectors:
            for el in self.driver.find_elements(By.CSS_SELECTOR, css):
                try:
                    if el.is_displayed() and (el.text or el.tag_name):
                        return
                except WebDriverException:
                    continue
        text = normalize_page_text(self._page_text())
        if any(s in text for s in ("©", "газпром", "правила использования", "политика")):
            return
        raise MincifryError(f"На странице Минцифр не отображается футер:{self._debug_where()}")

    def health_steps(self):
        return [
            ("landing_mincifry_banner", self.step_banner_visible),
            ("landing_mincifry_click", self.step_banner_clickable),
            ("landing_mincifry_yandex", self.step_yandex_browser_section),
            ("landing_mincifry_certs", self.step_certs_section),
            ("landing_mincifry_faq", self.step_faq_visible),
            ("landing_mincifry_faq_expand", self.step_faq_expandable),
            ("landing_mincifry_footer", self.step_footer_visible),
        ]

    def assert_full_flow(self) -> None:
        for _name, action in self.health_steps():
            action()
