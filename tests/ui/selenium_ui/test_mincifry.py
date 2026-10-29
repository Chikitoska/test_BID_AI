"""Страница Минцифр / российские сертификаты на лендинге."""

import pytest

from pages.mincifry_page import MincifryPage
from pages.landing_page import LandingPage


@pytest.mark.ui
@pytest.mark.selenium
def test_landing_mincifry_full_flow(landing_page: LandingPage):
    MincifryPage(landing_page.driver).assert_full_flow()
