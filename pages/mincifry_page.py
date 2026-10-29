"""Страница Минцифр / российские сертификаты на лендинге."""

from __future__ import annotations

import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.widget_urls import (
    is_blank_target,
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
    "частые вопросы",
    "часто задаваемые вопросы",
    "часто задаваемый вопрос",
    "вопросы и ответы",
    "faq",
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
        for snippet in snippets:
            xpath = f"//*[contains(normalize-space(.), '{snippet}')]"
            try:
                matches = self.driver.find_elements(By.XPATH, xpath)
            except WebDriverException:
                continue
            for el in matches:
                try:
                    if el.is_displayed():
                        return el
                except WebDriverException:
                    continue
            if matches:
                return matches[0]
        return None

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

    def _clickable_from(self, node):
        if node is None:
            return None
        tag = (node.tag_name or "").lower()
        if tag in {"a", "button"}:
            return node
        for xpath in (".//a", ".//button", "./ancestor::a[1]", "./ancestor::button[1]"):
            try:
                found = node.find_element(By.XPATH, xpath)
                if found:
                    return found
            except WebDriverException:
                continue
        return node

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
        target = self._clickable_from(banner)
        if target is None:
            raise MincifryError("Блок Минцифр на лендинге некликабелен")
        href = (target.get_attribute("href") or "").strip()
        if href and is_blank_target(href):
            raise MincifryError(f"Ссылка Минцифр ведёт в about:blank: {href!r}")

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

    def _faq_root(self):
        node = self._visible_by_texts(
            ("Частые вопросы", "Часто задаваемые вопросы", "Вопросы и ответы", "FAQ")
        )
        if node is None:
            return None
        for xpath in (
            "./ancestor::*[contains(@class,'faq') or contains(@class,'accordion') or contains(@class,'questions')][1]",
            "./ancestor::section[1]",
            "./ancestor::*[self::section or self::div][1]",
        ):
            try:
                return node.find_element(By.XPATH, xpath)
            except WebDriverException:
                continue
        return node

    def step_faq_visible(self) -> None:
        text = normalize_page_text(self._page_text())
        if self._faq_root() is None and not any(s in text for s in FAQ_SNIPPETS):
            raise MincifryError(
                "На странице Минцифр не отображается блок с частыми вопросами:"
                f"{self._debug_where()}"
            )

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
        return False

    def step_faq_expandable(self) -> None:
        root = self._faq_root()
        finder = root.find_elements if root is not None else self.driver.find_elements
        candidates = []
        try:
            candidates.extend(
                finder(
                    By.CSS_SELECTOR,
                    "details, summary, [aria-expanded], button, [role='button']",
                )
            )
        except WebDriverException:
            candidates = []
        clickable = []
        for el in candidates:
            try:
                if not el.is_displayed():
                    continue
            except WebDriverException:
                continue
            text = " ".join((el.text or "").split())[:80].lower()
            tag = (el.tag_name or "").lower()
            aria = (el.get_attribute("aria-expanded") or "").lower()
            if tag in {"summary", "details"} or aria in {"false", "true"} or "вопрос" in text:
                clickable.append(el)
        if not clickable:
            for el in candidates:
                try:
                    if el.is_displayed() and (el.tag_name or "").lower() in {"button", "summary", "a"}:
                        clickable.append(el)
                        break
                except WebDriverException:
                    continue
        if not clickable:
            raise MincifryError("Блок частых вопросов есть, но его нельзя раскрыть")

        target = clickable[0]
        before_len = len(self._page_text())
        already = self._is_expanded(target)
        try:
            self._click(target)
        except WebDriverException as exc:
            raise MincifryError(f"Не удалось раскрыть частый вопрос: {exc}") from exc
        time.sleep(0.6)
        after_len = len(self._page_text())
        if already or self._is_expanded(target) or after_len > before_len + 20:
            return
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
