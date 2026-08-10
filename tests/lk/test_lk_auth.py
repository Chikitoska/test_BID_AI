"""Pytest: авторизация и проверки ЛК (перенос из проекта BID)."""

from __future__ import annotations

import pytest

from config.lk_settings import BID_EXPECTED_COMPANY, BID_EXPECTED_FIO, BID_LK_EXPECTED_URL, BID_PROCESSOR_URL
from pages.lk_flow import LkFlow

pytestmark = pytest.mark.lk


def test_auth_redirects_to_lk(authenticated_driver):
    assert BID_LK_EXPECTED_URL in authenticated_driver.current_url


def test_company_name_in_lk(authenticated_driver):
    company = LkFlow(authenticated_driver).read_company_in_lk()
    assert company == BID_EXPECTED_COMPANY


def test_service_provider_opens(processor_driver):
    assert BID_PROCESSOR_URL in processor_driver.current_url


def test_fio_in_service_provider(processor_driver):
    assert LkFlow(processor_driver).read_fio_in_processor() == BID_EXPECTED_FIO


def test_company_in_service_provider(processor_driver):
    assert LkFlow(processor_driver).read_company_in_processor() == BID_EXPECTED_COMPANY
