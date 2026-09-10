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
    state, current = lk_page.accreditation_upgrade_path_state()
    if state == "page_error":
        pytest.fail("Раздел «Аккредитация» не загрузился или нет текущего уровня")
    if state == "max_level":
        pytest.skip(
            f"Нет доступных уровней выше текущего ({current}) — UI выбора не обязателен"
        )
    assert lk_page.accreditation_level_selection_available(), (
        "Не отображается UI выбора уровня аккредитации "
        "(карточки «ДОСТУПНО» или опросник «Выбрать уровень»)"
    )


def test_lk_accreditation_apply_button_without_submit(lk_page: LkPage):
    """Элемент начала выбора уровня виден, но анкету не отправляем."""
    state, current = lk_page.accreditation_upgrade_path_state()
    if state == "page_error":
        pytest.fail("Раздел «Аккредитация» не загрузился или нет текущего уровня")
    if state == "max_level":
        pytest.skip(
            f"Нет пути повышения уровня (текущий={current}) — кнопка выбора не обязательна"
        )
    assert lk_page.accreditation_apply_button_visible(), (
        "Не отображается элемент начала выбора уровня "
        "(«Заполнить анкету», «Выбрать уровень» или «Далее»)"
    )
