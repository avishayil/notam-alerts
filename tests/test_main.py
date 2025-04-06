import pytest

import main


@pytest.fixture
def mock_scraper(monkeypatch):
    monkeypatch.setattr(
        "src.scraper.NotamScraper.scrape",
        lambda self: [
            {
                "notam_id": "TEST123",
                "start_il": "2025-01-01 08:00",
                "end_il": "2025-01-01 20:00",
            }
        ],
    )


@pytest.fixture
def mock_data_handler(monkeypatch):
    monkeypatch.setattr("src.data_handler.NotamDataHandler.load", lambda self: [])
    monkeypatch.setattr(
        "src.data_handler.NotamDataHandler.save", lambda self, data: None
    )


@pytest.fixture
def mock_notifier(monkeypatch):
    monkeypatch.setattr(
        "src.notifier.NotamNotifier.send",
        lambda self, added, removed: print("Mock Notification Sent"),
    )


def test_main_runs_without_error(mock_scraper, mock_data_handler, mock_notifier):
    main.main()
