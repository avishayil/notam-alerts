import logging
from datetime import datetime

from src.constants import ISRAEL_TZ, UTC_TZ


def convert_zulu_to_israel(zulu_str: str) -> datetime:
    logging.debug(f"Converting Zulu time string: {zulu_str}")
    dt = datetime.strptime(zulu_str, "%y%m%d%H%M").replace(tzinfo=UTC_TZ)
    logging.debug(f"Parsed datetime in UTC: {dt.isoformat()}")
    dt_il = dt.astimezone(ISRAEL_TZ)
    logging.debug(f"Converted datetime in Israel timezone: {dt_il.isoformat()}")
    return dt_il
