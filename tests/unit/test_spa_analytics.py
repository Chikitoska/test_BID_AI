import pytest

from utils.spa_analytics import (
    DEFAULT_MONITOR_ANALYTICS_UID,
    events_uid_rewrite_js,
    extract_event_names_from_events_body,
    extract_uids_from_events_body,
    spa_events_cookie_header,
    spa_events_payload,
    spa_events_uid,
    stamp_events_uid_in_body,
    stamp_events_uid_in_payload,
)


def test_spa_events_payload_always_uses_monitor_uuid():
    payload = spa_events_payload()
    assert len(payload) == 1
    assert payload[0]["uid"] == spa_events_uid() == DEFAULT_MONITOR_ANALYTICS_UID
    assert payload[0]["event"] == "page_view"


@pytest.mark.parametrize(
    "event",
    (
        "page_view",
        "chat_open",
        "landing_assistant_open_chat",
        "landing_assistant_click_option",
        "lk_assistant_open_chat",
        "lk_assistant_click_option",
    ),
)
def test_spa_events_payload_chatbot_like_events_use_monitor_uuid(event):
    payload = spa_events_payload(event=event)
    assert payload[0]["uid"] == spa_events_uid() == DEFAULT_MONITOR_ANALYTICS_UID
    assert payload[0]["event"] == event


def test_spa_events_cookie_header_uses_same_uuid():
    assert spa_events_cookie_header().endswith(f"={DEFAULT_MONITOR_ANALYTICS_UID}")


def test_extract_uids_from_list_and_dict_bodies():
    listed = extract_uids_from_events_body(
        '[{"event":"page_view","counterId":1212,"uid":"b1d00000-0000-4000-a000-000000000001"}]'
    )
    wrapped = extract_uids_from_events_body(
        '{"uid":"b1d00000-0000-4000-a000-000000000001","events":[{"event":"page_view"}]}'
    )
    custom = extract_uids_from_events_body(
        '{"customUserId":"b1d00000-0000-4000-a000-000000000001"}'
    )
    expected = ["b1d00000-0000-4000-a000-000000000001"]
    assert listed == expected
    assert wrapped == expected
    assert custom == expected


def test_extract_event_names_from_chatbot_bodies():
    names = extract_event_names_from_events_body(
        '[{"event":"chat_open","uid":"b1d00000-0000-4000-a000-000000000001"},'
        '{"event":"chat_close","uid":"b1d00000-0000-4000-a000-000000000001"}]'
    )
    assert names == ["chat_open", "chat_close"]
    consta = extract_event_names_from_events_body(
        '{"eventType":3,"componentid":"landing_assistant_open_chat",'
        '"constaeventtype":"click","uid":"b1d00000-0000-4000-a000-000000000001"}'
    )
    assert consta == ["landing_assistant_open_chat:click"]


def test_stamp_replaces_foreign_uid_and_fills_missing():
    foreign = "aaaaaaaa-1111-4111-a111-111111111111"
    stamped = stamp_events_uid_in_body(
        f'[{{"event":"chat_open","counterId":1212,"uid":"{foreign}"}}]'
    )
    assert extract_uids_from_events_body(stamped) == [DEFAULT_MONITOR_ANALYTICS_UID]
    missing = stamp_events_uid_in_payload([{"event": "chat_close", "counterId": 1212}])
    assert missing[0]["uid"] == DEFAULT_MONITOR_ANALYTICS_UID


def test_extract_and_stamp_as_user_id_customparams():
    foreign = "e0f94430-377f-4d63-88ea-496faad5b610"
    body = (
        '{"eventType":3,"uid":"b1d00000-0000-4000-a000-000000000001",'
        f'"customparams":[{{"as_user_id":true,"value":"{foreign}"}}]}}'
    )
    assert foreign in extract_uids_from_events_body(body)
    stamped = stamp_events_uid_in_body(body)
    uids = extract_uids_from_events_body(stamped)
    assert uids
    assert all(uid == DEFAULT_MONITOR_ANALYTICS_UID for uid in uids)
    assert foreign not in uids


def test_events_uid_rewrite_js_embeds_monitor_uid_and_keys():
    js = events_uid_rewrite_js()
    assert DEFAULT_MONITOR_ANALYTICS_UID in js
    assert "spa-back.gazprom-neft.ru/events" in js
    assert "customUserId" in js
    assert "as_user_id" in js
    assert "window.fetch" in js
    assert "XMLHttpRequest" in js
    assert "sendBeacon" in js
