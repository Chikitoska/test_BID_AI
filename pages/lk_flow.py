"""Сценарий авторизации BID → ЛК → Processor (перенос из проекта BID, без секретов в коде)."""

from __future__ import annotations

import os
import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.lk_settings import (
    BID_LK_EXPECTED_URL,
    BID_PASSWORD,
    BID_PROCESSOR_URL,
    BID_TOTP_SECRET,
    BID_USERNAME,
    LANDING_BASE_URL,
    LK_AUTH_WAIT_SEC,
    LK_LOGIN_WAIT_SEC,
    LK_PROCESSOR_HEADER_ATTEMPTS,
    LK_PROCESSOR_HEADER_RETRY_DELAY_SEC,
    LK_SKIP_LANDING,
    LK_UI_WAIT_SEC,
)
from utils.lk_modals import accept_lk_consent_modals, accept_processor_consent_modals
from utils.totp import generate_totp_sha256


class LkAuthError(Exception):
    """Ошибка шага авторизации или проверки ЛК."""


class HttpStatusError(LkAuthError):
    """Страница ЛК с /error/4xx|/error/5xx — повторяемый prod-сигнал."""


class LkFlow:
    AUTH_URL_MARKERS = ("id.bid.gazprom-neft.ru", "openid-connect", "/realms/")

    def __init__(self, driver: WebDriver, *, wait_sec: int | None = None):
        self.driver = driver
        self.wait_sec = wait_sec or LK_LOGIN_WAIT_SEC

    def _log(self, message: str) -> None:
        print(f"[lk] {message}", flush=True)

    def _safe_click(self, element) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def _is_auth_url(self, url: str) -> bool:
        return any(marker in url for marker in self.AUTH_URL_MARKERS)

    def _in_lk(self) -> bool:
        return "lk.bid.gazprom-neft.ru" in self.driver.current_url

    def _find_visible(self, selectors: tuple[tuple[str, str], ...]):
        for by, value in selectors:
            for element in self.driver.find_elements(by, value):
                if element.is_displayed() and element.is_enabled():
                    return element
        return None

    def _open_keycloak_login(self) -> None:
        login_link = WebDriverWait(self.driver, self.wait_sec).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, 'self-authentication')]")
            )
        )
        auth_url = (login_link.get_attribute("href") or "").strip()
        if not auth_url:
            raise LkAuthError("Ссылка «Войти» без href")

        self._log(f"Переход на Keycloak: {auth_url[:80]}...")
        self.driver.get(auth_url)

        WebDriverWait(self.driver, self.wait_sec).until(
            lambda d: self._is_auth_url(d.current_url)
        )
        self._log(f"Keycloak открыт: {self.driver.current_url[:80]}...")

    def _set_input_value(self, element, value: str) -> None:
        """Keycloak (React) часто игнорирует send_keys — ставим value через JS."""
        self.driver.execute_script(
            """
            const input = arguments[0];
            const nextValue = arguments[1];
            input.focus();
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value'
            ).set;
            setter.call(input, nextValue);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            value,
        )

    def _input_value(self, element) -> str:
        return (
            self.driver.execute_script("return arguments[0].value || '';", element)
            or element.get_attribute("value")
            or ""
        )

    def _type_into(self, element, value: str, *, label: str) -> None:
        if not value:
            raise LkAuthError(f"Пустое значение для «{label}» — проверьте monitor/.env")

        self._safe_click(element)
        self._set_input_value(element, value)
        actual = self._input_value(element)

        if actual != value:
            element.clear()
            element.send_keys(value)
            actual = self._input_value(element)

        if actual != value:
            self._set_input_value(element, value)
            actual = self._input_value(element)

        if not actual:
            raise LkAuthError(f"Поле «{label}» не заполнилось")

        self._log(f"{label} заполнено ({len(actual)} символов)")

    def _lk_target_url(self) -> str:
        return os.getenv("BID_LK_EXPECTED_URL", BID_LK_EXPECTED_URL)

    def _on_target_lk(self, url: str | None = None) -> bool:
        current = url or self.driver.current_url
        target = self._lk_target_url()
        return "/service-providers" in current or target in current

    def _has_lk_session(self) -> bool:
        if "lk.bid.gazprom-neft.ru" not in self.driver.current_url:
            return False
        badges = self.driver.find_elements(
            By.CSS_SELECTOR, "[data-testid='md-user_badge']"
        )
        return any(badge.is_displayed() for badge in badges)

    def _wait_auth_or_lk_session(self) -> None:
        WebDriverWait(self.driver, self.wait_sec).until(
            lambda d: self._is_auth_url(d.current_url) or self._has_lk_session()
        )

    def _wait_clickable(self, selectors: tuple[tuple[str, str], ...]):
        for by, value in selectors:
            try:
                element = WebDriverWait(self.driver, self.wait_sec).until(
                    EC.element_to_be_clickable((by, value))
                )
                if element.is_displayed():
                    return element
            except Exception:
                continue
        return None

    def _open_auth_entry(self) -> None:
        if LK_SKIP_LANDING:
            target = self._lk_target_url()
            self._log("Открываем ЛК (редirect на Keycloak при необходимости)")
            self.driver.get(target)
            self._wait_auth_or_lk_session()
            if self._has_lk_session():
                self._log("Уже в ЛК")
            elif self._is_auth_url(self.driver.current_url):
                self._log(f"Keycloak открыт: {self.driver.current_url[:80]}...")
            else:
                raise LkAuthError(f"Не Keycloak и не ЛК (URL: {self.driver.current_url})")
            return

        self._log("Открываем лендинг")
        self.driver.get(LANDING_BASE_URL)
        self._open_keycloak_login()

    def _fill_credentials(self) -> None:
        username_selectors = (
            (By.ID, "username"),
            (By.NAME, "username"),
            (By.CSS_SELECTOR, "input[name='username']"),
        )
        password_selectors = (
            (By.ID, "password"),
            (By.NAME, "password"),
            (By.CSS_SELECTOR, "input[name='password']"),
        )
        submit_selectors = (
            (By.ID, "kc-login"),
            (By.NAME, "login"),
            (By.CSS_SELECTOR, "#kc-login"),
            (By.CSS_SELECTOR, "input[type='submit']"),
        )

        username_el = self._wait_clickable(username_selectors)
        if username_el is None:
            raise LkAuthError(f"Нет поля логина (URL: {self.driver.current_url})")

        username = os.getenv("BID_USERNAME", BID_USERNAME).strip()
        password = os.getenv("BID_PASSWORD", BID_PASSWORD).strip()

        self._log("Ввод логина")
        self._type_into(username_el, username, label="Логин")

        password_el = self._wait_clickable(password_selectors)
        if password_el is None:
            raise LkAuthError(f"Нет поля пароля (URL: {self.driver.current_url})")

        self._log("Ввод пароля")
        self._type_into(password_el, password, label="Пароль")

        submit_el = self._wait_clickable(submit_selectors)
        if submit_el is None:
            raise LkAuthError("Нет кнопки входа Keycloak")

        self._log("Отправка формы логина")
        self._safe_click(submit_el)

    def _keycloak_error(self) -> str:
        selectors = (
            ".kc-feedback-text",
            ".alert-error",
            "#input-error",
            "span[id^='input-error']",
            ".pf-c-form__helper-text.pf-m-error",
        )
        for selector in selectors:
            for element in self.driver.find_elements(By.CSS_SELECTOR, selector):
                text = (element.text or element.get_attribute("innerText") or "").strip()
                if text:
                    return text
        return ""

    def _wait_for_otp_field(self):
        self._log("Ожидание поля OTP (или редиректа в ЛК)...")
        otp_selectors = (
            (By.ID, "otp"),
            (By.ID, "totp"),
            (By.NAME, "otp"),
            (By.NAME, "totp"),
            (By.CSS_SELECTOR, "input[autocomplete='one-time-code']"),
        )
        deadline = time.time() + self.wait_sec
        while time.time() < deadline:
            if self._has_lk_session():
                return None

            error = self._keycloak_error()
            if error:
                raise LkAuthError(f"Keycloak: {error}")

            for by, value in otp_selectors:
                for element in self.driver.find_elements(by, value):
                    if element.is_displayed():
                        return element
            time.sleep(0.2)

        raise LkAuthError(
            f"Нет поля OTP за {self.wait_sec} с (URL: {self.driver.current_url})"
        )

    def _submit_otp_if_needed(self) -> None:
        otp_field = self._wait_for_otp_field()
        if otp_field is None:
            return

        self._log("Ввод OTP")
        totp_secret = os.getenv("BID_TOTP_SECRET", BID_TOTP_SECRET).strip()
        if not totp_secret:
            raise LkAuthError("BID_TOTP_SECRET пустой — проверьте monitor/.env")
        otp_code = generate_totp_sha256(totp_secret)
        self._type_into(otp_field, otp_code, label="OTP")
        submit_el = self._find_visible((
            (By.ID, "kc-login"),
            (By.NAME, "login"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.CSS_SELECTOR, "button[type='submit']"),
        ))
        if submit_el is not None:
            self._safe_click(submit_el)

        WebDriverWait(self.driver, LK_AUTH_WAIT_SEC).until(
            lambda d: "lk.bid.gazprom-neft.ru" in d.current_url or self._keycloak_error()
        )
        error = self._keycloak_error()
        if error:
            raise LkAuthError(f"Keycloak после OTP: {error}")

    def _ensure_lk_ready(self) -> None:
        """Ждём бейдж пользователя; модалки согласия закрываем по ходу."""
        ready_sec = max(self.wait_sec, LK_UI_WAIT_SEC)
        deadline = time.time() + ready_sec
        while time.time() < deadline:
            accept_lk_consent_modals(self.driver, timeout=3)
            url = self.driver.current_url or ""
            if re.search(r"/error/(4\d{2}|5\d{2})\b", url, flags=re.I):
                raise HttpStatusError(
                    f"ЛК вернул HTTP error page после входа, URL: {url[:160]}"
                )
            if self._has_lk_session():
                return
            time.sleep(0.3)

        url = self.driver.current_url
        if re.search(r"/error/(4\d{2}|5\d{2})\b", url or "", flags=re.I):
            raise HttpStatusError(
                f"ЛК вернул HTTP error page после входа, URL: {url[:160]}"
            )
        raise LkAuthError(
            f"ЛК не загрузился после входа (нет бейджа пользователя), URL: {url[:120]}"
        )

    def _ensure_on_lk_page(self) -> str:
        lk_url = self._lk_target_url()

        if self._on_target_lk() and self._has_lk_session():
            accept_lk_consent_modals(self.driver)
            return self.driver.current_url

        WebDriverWait(self.driver, LK_AUTH_WAIT_SEC).until(
            lambda d: "lk.bid.gazprom-neft.ru" in d.current_url
        )

        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: self._on_target_lk(d.current_url)
            )
        except Exception:
            self._log(f"Переход в раздел ЛК: {lk_url}")
            self.driver.get(lk_url)
            WebDriverWait(self.driver, self.wait_sec).until(
                lambda d: self._on_target_lk(d.current_url)
            )

        self._ensure_lk_ready()
        return self.driver.current_url

    def login(self) -> str:
        """Полный вход до целевой страницы ЛК."""
        self._open_auth_entry()
        if not self._has_lk_session():
            self._fill_credentials()
            self._submit_otp_if_needed()
        return self._ensure_on_lk_page()

    def login_from_landing(self) -> None:
        self.login()

    def wait_for_lk_redirect(self) -> str:
        return self._ensure_on_lk_page()

    def read_company_in_lk(self) -> str:
        wait_sec = max(self.wait_sec, LK_UI_WAIT_SEC)
        if "/service-providers" not in self.driver.current_url:
            self.driver.get(self._lk_target_url())
        accept_lk_consent_modals(self.driver)
        company_elem = WebDriverWait(self.driver, wait_sec).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='md-user_badge'] .User-Info")
            )
        )
        return company_elem.text.strip()

    def open_service_provider(self) -> None:
        wait_sec = max(self.wait_sec, LK_UI_WAIT_SEC)
        if "/service-providers" not in self.driver.current_url:
            self.driver.get(self._lk_target_url())
            accept_lk_consent_modals(self.driver)

        sp_button = WebDriverWait(self.driver, wait_sec).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[contains(text(), 'Processor. Модуль приема предложений')]"
                    "/parent::div/parent::div//button",
                )
            )
        )
        original_windows = self.driver.window_handles
        self._safe_click(sp_button)

        WebDriverWait(self.driver, wait_sec).until(
            lambda d: len(d.window_handles) > len(original_windows)
        )
        new_window = [wh for wh in self.driver.window_handles if wh not in original_windows][0]
        self.driver.switch_to.window(new_window)

        WebDriverWait(self.driver, wait_sec).until(
            lambda d: BID_PROCESSOR_URL in d.current_url
        )
        self._ensure_processor_header_ready()

    def _ensure_processor_header_ready(self) -> None:
        """Модалки + мягкое ожидание шапки User-Block (без жёсткого fail)."""
        wait_sec = min(20, max(self.wait_sec, LK_UI_WAIT_SEC))
        accept_processor_consent_modals(self.driver, timeout=5)
        try:
            WebDriverWait(self.driver, wait_sec).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".User-Block, [class='User-Block']")
                )
            )
        except TimeoutException:
            self._log(
                f"Processor: User-Block ещё не виден за {wait_sec}s "
                f"(URL={self.driver.current_url}), чтение ФИО/компании повторит ожидание"
            )
    def _read_processor_user_field(self, *, css_child: str, label: str) -> str:
        """Читает поле в шапке Processor с повтором (модалки / медленный SPA)."""
        wait_sec = max(self.wait_sec, LK_UI_WAIT_SEC)
        selectors = (
            f".User-Block {css_child}",
            f"[class='User-Block'] {css_child}",
        )
        attempts = max(1, LK_PROCESSOR_HEADER_ATTEMPTS)
        last_error: Exception | None = None

        for attempt in range(1, attempts + 1):
            accept_processor_consent_modals(self.driver, timeout=3)
            for selector in selectors:
                try:
                    element = WebDriverWait(self.driver, wait_sec).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    text = (element.text or "").strip()
                    if text:
                        return text
                    last_error = TimeoutException(
                        f"Processor: «{label}» пустой ({selector}). URL={self.driver.current_url}"
                    )
                except TimeoutException as exc:
                    last_error = exc

            self._log(
                f"Processor: «{label}» не готово "
                f"({attempt}/{attempts}), повтор через {LK_PROCESSOR_HEADER_RETRY_DELAY_SEC}s"
            )
            if attempt < attempts:
                time.sleep(LK_PROCESSOR_HEADER_RETRY_DELAY_SEC)

        detail = str(last_error) if last_error else "элемент не найден"
        raise TimeoutException(
            f"Processor: не видно «{label}» ({css_child}) после {attempts} попыток "
            f"по {wait_sec}s. URL={self.driver.current_url}. {detail}"
        )

    def read_fio_in_processor(self) -> str:
        return self._read_processor_user_field(css_child=".User-Name", label="ФИО")

    def read_company_in_processor(self) -> str:
        return self._read_processor_user_field(css_child=".User-Info", label="компания")
