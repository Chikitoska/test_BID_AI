import pytest

from utils.spa_analytics import DEFAULT_MONITOR_ANALYTICS_UID
from utils.spa_events_sniffer import (
    SpaEventPost,
    SpaEventsUidError,
    assert_only_monitor_uid,
)


EXPECTED = DEFAULT_MONITOR_ANALYTICS_UID
FOREIGN = "cccccccc-2222-4222-a222-222222222222"


def test_assert_only_monitor_uid_passes_on_expected():
    posts = [
        SpaEventPost(
            body='[{"event":"chat_open","uid":"%s"}]' % EXPECTED,
            uids=[EXPECTED],
            event_names=["chat_open"],
        )
    ]
    assert_only_monitor_uid(posts, expected=EXPECTED)


def test_assert_only_monitor_uid_fails_on_foreign():
    posts = [
        SpaEventPost(
            body='[{"event":"chat_open","uid":"%s"}]' % FOREIGN,
            uids=[FOREIGN],
            event_names=["chat_open"],
        )
    ]
    with pytest.raises(SpaEventsUidError, match="чужие uid"):
        assert_only_monitor_uid(posts, expected=EXPECTED)


def test_assert_only_monitor_uid_fails_on_as_user_id_foreign():
    posts = [
        '{"uid":"%s","customparams":[{"as_user_id":true,"value":"%s"}]}'
        % (EXPECTED, FOREIGN)
    ]
    with pytest.raises(SpaEventsUidError, match="чужие uid"):
        assert_only_monitor_uid(posts, expected=EXPECTED)


def test_assert_only_monitor_uid_fails_when_missing_uid():
    posts = [
        SpaEventPost(
            body='[{"event":"chat_open","counterId":1212}]',
            uids=[],
            event_names=["chat_open"],
        )
    ]
    with pytest.raises(SpaEventsUidError, match="без uid"):
        assert_only_monitor_uid(posts, expected=EXPECTED)


def test_assert_only_monitor_uid_fails_when_no_posts():
    with pytest.raises(SpaEventsUidError, match="не обнаружен"):
        assert_only_monitor_uid([], expected=EXPECTED, require_posts=True)


def test_assert_only_monitor_uid_accepts_raw_bodies():
    body = '[{"event":"page_view","uid":"%s"}]' % EXPECTED
    assert_only_monitor_uid([body], expected=EXPECTED)
