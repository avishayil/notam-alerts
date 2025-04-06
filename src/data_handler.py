import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple

from src.constants import NOTAM_FILE

NOTAM = Dict[str, str]


class NotamDataHandler:
    def load(self, filepath: str = NOTAM_FILE) -> List[NOTAM]:
        logging.debug(f"Attempting to load NOTAMs from {filepath}")
        if Path(filepath).exists():
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    logging.info(f"Loaded {len(data)} NOTAMs from {filepath}")
                    logging.debug(f"Loaded data: {data}")
                    return data
            except Exception as e:
                logging.error(f"Error loading data from {filepath}: {e}")
        else:
            logging.debug(f"File {filepath} does not exist.")
        return []

    def save(self, data: List[NOTAM], filepath: str = NOTAM_FILE) -> None:
        logging.debug(f"Attempting to save {len(data)} NOTAMs to {filepath}")
        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
                logging.info(f"Saved {len(data)} NOTAMs to {filepath}")
                logging.debug(f"Saved data: {data}")
        except Exception as e:
            logging.error(f"Error saving data to {filepath}: {e}")

    def detect_changes(
        self, prev: List[NOTAM], current: List[NOTAM]
    ) -> Tuple[List[NOTAM], List[NOTAM]]:
        logging.debug(
            f"Detecting changes between previous ({len(prev)}) and current ({len(current)}) NOTAMs"
        )
        prev_set = {json.dumps(x, sort_keys=True) for x in prev}
        curr_set = {json.dumps(x, sort_keys=True) for x in current}

        added = [json.loads(x) for x in curr_set - prev_set]
        removed = [json.loads(x) for x in prev_set - curr_set]

        logging.info(f"Detected {len(added)} added and {len(removed)} removed NOTAMs.")
        logging.debug(f"Added NOTAMs: {added}")
        logging.debug(f"Removed NOTAMs: {removed}")
        return added, removed
