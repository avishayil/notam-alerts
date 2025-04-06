from src.utils import convert_zulu_to_israel


def test_convert_zulu_to_israel():
    dt = convert_zulu_to_israel("2501010800")  # YYMMDDHHMM
    assert (
        dt.strftime("%Y-%m-%d %H:%M") == "2025-01-01 10:00"
    )  # Israel is UTC+2 in winter
