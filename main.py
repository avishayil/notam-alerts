import logging
import os

from src.data_handler import NotamDataHandler
from src.notifier import NotamNotifier
from src.scraper import NotamScraper


def main():
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logging.basicConfig(
        level=log_level, format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logging.debug("Starting NOTAM monitoring script...")

    scraper = NotamScraper()
    data_handler = NotamDataHandler()
    notifier = NotamNotifier()

    logging.debug("Scraping current NOTAMs...")
    current = scraper.scrape()
    logging.debug(f"Scraped {len(current)} current NOTAMs.")

    logging.debug("Loading previous NOTAMs from file...")
    previous = data_handler.load()
    logging.debug(f"Loaded {len(previous)} previous NOTAMs.")

    logging.debug("Detecting changes between previous and current NOTAMs...")
    added, removed = data_handler.detect_changes(previous, current)

    if added or removed:
        logging.debug(
            "Changes detected. Sending notifications and saving current data..."
        )
        notifier.send(added, removed)
        data_handler.save(current)
    else:
        logging.info("No changes detected. No notification sent.")

    logging.debug("Script execution completed.")


if __name__ == "__main__":
    main()
