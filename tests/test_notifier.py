import pytest

from src.notifier import NotamNotifier


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token")
    monkeypatch.setenv("TELEGRAM_CHANNEL_ID", "@fake-channel")


def test_compose_message():
    notifier = NotamNotifier()
    added = [
        {
            "notam_id": "ABC",
            "start_il": "2025-01-01 08:00",
            "end_il": "2025-01-01 20:00",
        }
    ]
    removed = []
    msg = notifier._compose_message(added, removed)
    assert "ABC" in msg
    assert "🟢" in msg
