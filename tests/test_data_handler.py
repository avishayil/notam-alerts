import tempfile

from src.data_handler import NotamDataHandler

mock_notams = [
    {
        "notam_id": "ABC123",
        "start_il": "2025-01-01 08:00",
        "end_il": "2025-01-01 20:00",
    },
    {
        "notam_id": "DEF456",
        "start_il": "2025-01-02 08:00",
        "end_il": "2025-01-02 20:00",
    },
]


def test_save_and_load():
    handler = NotamDataHandler()
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        handler.save(mock_notams, temp.name)
        loaded = handler.load(temp.name)
        assert loaded == mock_notams


def test_detect_changes():
    handler = NotamDataHandler()
    added, removed = handler.detect_changes(mock_notams[:1], mock_notams)
    assert len(added) == 1
    assert len(removed) == 0
