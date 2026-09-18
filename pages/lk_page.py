"""Страница ЛК (витрина сервисов) — smoke-проверки для мониторинга."""

from __future__ import annotations

import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.lk_settings import LK_UI_WAIT_SEC
from utils.lk_modals import accept_lk_consent_modals


class LkPageError(Exception):
    """Ошибка проверки UI личного кабинета."""


class LkPage:
    HEADER = "[data-testid='md-header']"
    NAVBAR = "[data-testid='md-navbar']"
    CONTENT = "[data-testid='md-content']"
    FOOTER = "[data-testid='md-footer']"
    USER_BADGE = "[data-testid='md-user_badge']"
    BTN_WRITE_US = "[data-testid='btn-write_us']"
    BTN_HELP = "[data-testid='btn-help-page']"

    NAV_ITEMS = ("Витрина", "Профиль компании", "Аккредитация", "Заявки")
    FOOTER_LINK_TEXTS = ("Правила использования", "Политика обработки персональных данных")
    VITRINA_URL_PART = "/service-providers"
    ACCREDITATION_URL_PART = "accreditation"
    PROCESSOR_MARKER = "Processor. Модуль приема предложений"
    MIN_CONTENT_LEN = 20
    CURRENT_LEVEL_RE = re.compile(r"ВЫ НА УРОВНЕ\s+(\d+)", re.IGNORECASE)
    ACCREDITED_LEVEL_RE = re.compile(r"аккредитована:\s*УРОВЕНЬ\s+(\d+)", re.IGNORECASE)
    # Новый UI: «УРОВЕНЬ БАЗОВЫЙ» вместо «УРОВЕНЬ 1»
    ACCREDITED_NAMED_RE = re.compile(
        r"УРОВЕНЬ\s+(БАЗОВЫЙ|СТАНДАРТНЫЙ|РАСШИРЕННЫЙ|ПРЕМИУМ|\d+)",
        re.IGNORECASE,
    )
    LEVEL_NAME_TO_NUM = {
        "БАЗОВЫЙ": 1,
        "СТАНДАРТНЫЙ": 2,
        "РАСШИРЕННЫЙ": 3,
        "ПРЕМИУМ": 4,
    }

    SECTIONS = (
        ("Витрина", VITRINA_URL_PART),
        ("Аккредитация", ACCREDITATION_URL_PART),
    )

    def __init__(self, driver: WebDriver, *, wait_sec: int | None = None):
        self.driver = driver
        self.wait_sec = wait_sec or LK_UI_WAIT_SEC
        self.wait = WebDriverWait(driver, self.wait_sec)
        self.last_section: str | None = None
        self._accreditation_content_cache: str | None = None

    def _clear_accreditation_cache(self) -> None:
        self._accreditation_content_cache = None

    def _visible(self, css: str):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))

    def dismiss_consent_modals(self) -> bool:
        return accept_lk_consent_modals(self.driver, timeout=self.wait_sec)

    def wait_ready(self) -> None:
        self.dismiss_consent_modals()
        self._visible(self.USER_BADGE)
        self.dismiss_consent_modals()

    def shell_blocks_visible(self) -> dict[str, bool]:
        blocks = (self.HEADER, self.NAVBAR, self.CONTENT, self.FOOTER, self.USER_BADGE)
        return {
            selector: any(el.is_displayed() for el in self.driver.find_elements(By.CSS_SELECTOR, selector))
            for selector in blocks
        }

    def read_user_fio(self) -> str:
        element = self._visible(f"{self.USER_BADGE} .User-Name")
        return element.text.strip()

    def read_user_company(self) -> str:
        element = self._visible(f"{self.USER_BADGE} .User-Info")
        return element.text.strip()

    def nav_items(self) -> list[str]:
        navbar = self._visible(self.NAVBAR)
        items = [line.strip() for line in navbar.text.splitlines() if line.strip()]
        return items

    def header_buttons_visible(self) -> dict[str, bool]:
        result: dict[str, bool] = {}
        for testid in (self.BTN_WRITE_US, self.BTN_HELP):
            elements = self.driver.find_elements(By.CSS_SELECTOR, testid)
            result[testid] = any(el.is_displayed() and el.is_enabled() for el in elements)
        return result

    def footer_link_texts(self) -> list[str]:
        footer = self._visible(self.FOOTER)
        links = footer.find_elements(By.CSS_SELECTOR, "a")
        return [link.text.strip() for link in links if link.is_displayed() and link.text.strip()]

    def click_nav_item(self, title: str) -> None:
        navbar = self._visible(self.NAVBAR)
        candidates = navbar.find_elements(
            By.XPATH, f".//*[normalize-space(text())='{title}']"
        )
        for element in candidates:
            if element.is_displayed():
                self.driver.execute_script("arguments[0].click();", element)
                return
        raise LkPageError(f"Пункт меню «{title}» не найден")

    def wait_url_contains(self, part: str) -> None:
        self.wait.until(lambda d: part in d.current_url)

    def open_section(self, title: str, url_part: str) -> None:
        if url_part != self.ACCREDITATION_URL_PART:
            self._clear_accreditation_cache()
        if url_part not in self.driver.current_url:
            self.click_nav_item(title)
            self.wait_url_contains(url_part)
        self.dismiss_consent_modals()
        self.last_section = title

    def open_vitrina(self) -> None:
        self.open_section("Витрина", self.VITRINA_URL_PART)

    def open_accreditation(self) -> None:
        self.open_section("Аккредитация", self.ACCREDITATION_URL_PART)

    def read_accreditation_content(self) -> str:
        if self._accreditation_content_cache is not None:
            return self._accreditation_content_cache
        self.open_accreditation()
        # Раздел «Аккредитация» на VPS headless грузится дольше после длинной сессии.
        content = self.content_with_timeout(timeout=max(self.wait_sec, 45))
        self._accreditation_content_cache = content
        return content

    def _parse_accreditation_level(self, content: str) -> int:
        for pattern in (self.CURRENT_LEVEL_RE, self.ACCREDITED_LEVEL_RE):
            match = pattern.search(content)
            if match:
                return int(match.group(1))

        match = self.ACCREDITED_NAMED_RE.search(content)
        if match:
            token = match.group(1).upper()
            if token.isdigit():
                return int(token)
            return self.LEVEL_NAME_TO_NUM.get(token, 1)

        return 0

    def _level_token_to_num(self, token: str) -> int | None:
        token = token.upper()
        if token.isdigit():
            return int(token)
        return self.LEVEL_NAME_TO_NUM.get(token)

    def _parse_legacy_selectable_levels(self, content: str) -> list[int]:
        """Карточки «ДОСТУПНО» — и «УРОВЕНЬ 2», и «УРОВЕНЬ СТАНДАРТНЫЙ»."""
        selectable: list[int] = []
        matches = list(self.ACCREDITED_NAMED_RE.finditer(content))
        for i, match in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            part = content[match.start() : end]
            if "ДОСТУПНО" not in part:
                continue
            num = self._level_token_to_num(match.group(1))
            if num:
                selectable.append(num)
        return sorted(set(selectable))

    def _wizard_selection_available(self, content: str) -> bool:
        """Новый UI: опросник для подбора уровня (без отправки анкеты)."""
        return (
            "Выбрать уровень" in content
            and "Далее" in content
            and (
                "Вы планируете" in content
                or "аккредитации требуется" in content.lower()
            )
        )

    def read_accreditation_levels(self) -> tuple[int, list[int]]:
        """Текущий уровень и доступные для выбора — одна загрузка страницы."""
        content = self.read_accreditation_content()
        current = self._parse_accreditation_level(content)
        if current < 1:
            raise LkPageError("Не отображается текущий уровень аккредитации")

        selectable = self._parse_legacy_selectable_levels(content)
        if selectable:
            return current, selectable

        # Новый UI: карточек «ДОСТУПНО» нет — есть опросник «Далее»
        if self._wizard_selection_available(content):
            return current, [current + 1]

        return current, []

    def read_current_accreditation_level(self) -> int:
        content = self.read_accreditation_content()
        level = self._parse_accreditation_level(content)
        if level >= 1:
            return level
        raise LkPageError("Не отображается текущий уровень аккредитации")

    def read_selectable_accreditation_levels(self) -> list[int]:
        """Уровни, помеченные как «ДОСТУПНО» для выбора (без клика и заполнения)."""
        return self._parse_legacy_selectable_levels(self.read_accreditation_content())

    def accreditation_level_selection_visible(self) -> bool:
        return self.accreditation_level_selection_available()

    def accreditation_level_selection_available(self) -> bool:
        """UI выбора уровня доступен (legacy-карточки или новый опросник)."""
        try:
            current, selectable = self.read_accreditation_levels()
        except (TimeoutException, LkPageError):
            return False
        return any(level > current for level in selectable)

    def accreditation_upgrade_path_state(self) -> tuple[str, int]:
        """Состояние апгрейда: available | max_level | page_error. Второе значение — текущий уровень (0 при ошибке)."""
        try:
            current, selectable = self.read_accreditation_levels()
        except (TimeoutException, LkPageError):
            return "page_error", 0
        if any(level > current for level in selectable):
            return "available", current
        return "max_level", current

    def accreditation_apply_button_visible(self) -> bool:
        """Признак начала выбора уровня: «Заполнить анкету», «Выбрать уровень» или «Далее»."""
        button_texts = ("Заполнить анкету", "Выбрать уровень", "Далее")
        try:
            content = self.read_accreditation_content()
        except (TimeoutException, LkPageError):
            return False
        if any(text in content for text in button_texts):
            return True
        return self._wizard_selection_available(content)

    def content_with_timeout(self, *, timeout: int | None = None) -> str:
        wait = WebDriverWait(self.driver, timeout or self.wait_sec)

        def _has_content(driver: WebDriver) -> bool:
            elements = driver.find_elements(By.CSS_SELECTOR, self.CONTENT)
            if not elements:
                return False
            return len(elements[0].text.strip()) >= self.MIN_CONTENT_LEN

        wait.until(_has_content)
        return self.driver.find_element(By.CSS_SELECTOR, self.CONTENT).text.strip()

    def try_section_content(self, title: str, url_part: str, *, timeout: int = 8) -> str | None:
        try:
            self.open_section(title, url_part)
            return self.content_with_timeout(timeout=timeout)
        except (TimeoutException, LkPageError):
            return None

    def ensure_section_with_content(self) -> tuple[str, str]:
        """Витрина → Аккредитация. Возвращает первый раздел с непустым контентом."""
        errors: list[str] = []
        for title, url_part in self.SECTIONS:
            content = self.try_section_content(title, url_part)
            if content:
                return title, content
            errors.append(title)

        raise LkPageError(
            f"Не загрузился ни один раздел ЛК (пробовали: {', '.join(errors)})"
        )

    def vitrina_content_loaded(self) -> str:
        self.open_vitrina()
        return self.content_with_timeout()

    def processor_card_visible(self) -> bool:
        if self.last_section != "Витрина":
            self.open_vitrina()
        try:
            content = self.content_with_timeout(timeout=8)
        except TimeoutException:
            return False
        return self.PROCESSOR_MARKER in content

    def on_vitrina(self) -> bool:
        return self.VITRINA_URL_PART in self.driver.current_url
