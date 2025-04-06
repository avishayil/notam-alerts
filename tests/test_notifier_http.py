import pytest
import requests_mock

from src.notifier import NotamNotifier


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")
    monkeypatch.setenv("TELEGRAM_CHANNEL_ID", "@test_channel")


def test_send_notification_success():
    notifier = NotamNotifier()
    added = [
        {
            "notam_id": "XYZ",
            "start_il": "2025-01-01 08:00",
            "end_il": "2025-01-01 20:00",
        }
    ]
    removed = []

    with requests_mock.Mocker() as m:
        m.post("https://api.telegram.org/bottest_token/sendMessage", json={"ok": True})
        notifier.send(added, removed)
        assert m.called
        assert m.call_count == 1
