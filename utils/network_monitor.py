"""Сбор сетевых запросов из Selenium (Chrome performance log)."""

import json

from utils.auth_filter import is_auth_url


def collect_network_responses(driver) -> list[dict]:
    """Возвращает список {url, status} из performance log Chrome."""
    responses: list[dict] = []
    for entry in driver.get_log("performance"):
        try:
            message = json.loads(entry["message"])["message"]
        except (KeyError, json.JSONDecodeError):
            continue
        if message.get("method") != "Network.responseReceived":
            continue
        payload = message.get("params", {}).get("response", {})
        url = payload.get("url", "")
        status = payload.get("status")
        if url and status is not None:
            responses.append({"url": url, "status": status})
    return responses


def collect_non_auth_responses(driver) -> list[dict]:
    return [item for item in collect_network_responses(driver) if not is_auth_url(item["url"])]
