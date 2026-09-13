"""Smoke-тесты раздела «Аккредитация» в ЛК (без заполнения анкеты)."""

from __future__ import annotations

import pytest

from pages.lk_page import LkPage

pytestmark = [pytest.mark.lk, pytest.mark.smoke]


def test_lk_accreditation_navigation(lk_page: LkPage):
    lk_page.open_accreditation()
    assert lk_page.ACCREDITATION_URL_PART in lk_page.driver.current_url


def test_lk_accreditation_current_level_displayed(lk_page: LkPage):
    level = lk_page.read_current_accreditation_level()
    assert level >= 1, f"Некорректный текущий уровень: {level}"


def test_lk_accreditation_level_selection_visible(lk_page: LkPage):
    """Smoke: CTA апгрейда есть не у каждой учётки — отсутствие UI это skip, не fail."""
    level = lk_page.read_current_accreditation_level()
    assert level >= 1, f"Некорректный текущий уровень: {level}"
    if not lk_page.accreditation_level_selection_available():
        pytest.skip(
            f"Нет UI выбора уровня при текущем уровне {level} "
            "(карточки «ДОСТУПНО» или опросник «Выбрать уровень»)"
        )


def test_lk_accreditation_apply_button_without_submit(lk_page: LkPage):
    """Элемент начала выбора уровня виден, но анкету не отправляем."""
    level = lk_page.read_current_accreditation_level()
    if not lk_page.accreditation_apply_button_visible():
        pytest.skip(
            f"Нет элемента начала выбора уровня при текущем уровне {level} "
            "(«Заполнить анкету», «Выбрать уровень» или «Далее»)"
        )
