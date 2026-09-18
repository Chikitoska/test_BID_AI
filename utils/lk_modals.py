"""Согласия в модальных окнах после входа в ЛК / СП."""

from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


def _accept_modal_checkboxes(modal, driver: WebDriver, *, submit_css: str) -> bool:
    checkboxes = modal.find_elements(
        By.CSS_SELECTOR, "input.Checkbox-Input.MixFocus[type='checkbox']"
    )
    toggled = False
    for checkbox in checkboxes:
        if checkbox.is_enabled() and checkbox.is_displayed() and not checkbox.is_selected():
            driver.execute_script("arguments[0].click();", checkbox)
            toggled = True

    if not toggled:
        return False

    submit = modal.find_element(By.CSS_SELECTOR, submit_css)
    driver.execute_script("arguments[0].click();", submit)
    return True


def accept_lk_consent_modals(driver: WebDriver, *, timeout: int = 8, max_rounds: int = 5) -> bool:
    """Закрывает модалку с правовыми документами (все галочки + «Отправить»).

    Модалка может появиться с задержкой после загрузки SPA — опрашиваем несколько раз.
    """
    accepted = False
    deadline = time.time() + timeout
    rounds = 0

    while time.time() < deadline and rounds < max_rounds:
        rounds += 1
        modals = [
            modal
            for modal in driver.find_elements(By.CSS_SELECTOR, "div[class*='_modal_']")
            if modal.is_displayed()
        ]
        if not modals:
            if accepted:
                return True
            time.sleep(0.3)
            continue

        if _accept_modal_checkboxes(modals[0], driver, submit_css="button[type='submit']"):
            accepted = True
        time.sleep(0.3)

    return accepted


def accept_processor_consent_modals(driver: WebDriver, *, timeout: int = 5) -> None:
    """Закрывает согласие Processor («Продолжить»), если окно появилось с задержкой."""
    deadline = time.time() + max(0.5, float(timeout))
    while time.time() < deadline:
        try:
            modals = [
                modal
                for modal in driver.find_elements(By.CSS_SELECTOR, "div[class*='Modal-Window']")
                if modal.is_displayed()
            ]
            if not modals:
                time.sleep(0.25)
                continue

            modal = modals[0]
            checkboxes = modal.find_elements(
                By.CSS_SELECTOR, "input.Checkbox-Input.MixFocus[type='checkbox']"
            )
            for checkbox in checkboxes:
                if checkbox.is_enabled() and checkbox.is_displayed() and not checkbox.is_selected():
                    try:
                        checkbox.click()
                    except Exception:
                        driver.execute_script("arguments[0].click();", checkbox)

            buttons = driver.find_elements(
                By.XPATH,
                "//button[contains(@class, 'Button') and contains(., 'Продолжить')]",
            )
            clicked = False
            for button in buttons:
                if button.is_displayed() and button.is_enabled():
                    try:
                        button.click()
                    except Exception:
                        driver.execute_script("arguments[0].click();", button)
                    clicked = True
                    break
            if clicked:
                time.sleep(0.4)
                return
        except Exception:
            pass
        time.sleep(0.25)
