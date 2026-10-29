from utils.spa_analytics import (
    DEFAULT_MONITOR_ANALYTICS_UID,
    extract_uids_from_events_body,
    spa_events_cookie_header,
    spa_events_payload,
    spa_events_uid,
)


def test_spa_events_payload_always_uses_monitor_uuid():
    payload = spa_events_payload()
    assert len(payload) == 1
    assert payload[0]["uid"] == spa_events_uid() == DEFAULT_MONITOR_ANALYTICS_UID
    assert payload[0]["event"] == "page_view"


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
