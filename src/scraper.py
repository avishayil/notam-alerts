import logging
import re
from typing import Dict, List

from playwright.sync_api import sync_playwright

from src.utils import convert_zulu_to_israel

NOTAM = Dict[str, str]


class NotamScraper:
    def scrape(self) -> List[NOTAM]:
        logging.info("Starting NOTAM scraping...")
        results = []

        with sync_playwright() as p:
            logging.debug("Launching Firefox browser...")
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()
            logging.debug("Navigating to NOTAM page...")
            page.goto(
                "https://brin.iaa.gov.il/aeroinfo/AeroInfo.aspx?msgType=Notam",
                timeout=60000,
            )
            page.wait_for_timeout(5000)

            logging.debug("Looking for relevant suffixes...")
            suffixes = self._find_relevant_suffixes(page)
            logging.debug(f"Found {len(suffixes)} relevant suffixes: {suffixes}")

            for suffix in suffixes:
                logging.debug(f"Extracting NOTAM for suffix: {suffix}")
                result = self._extract_notam(page, suffix)
                if result:
                    logging.debug(f"Extracted NOTAM: {result}")
                    results.append(result)
                else:
                    logging.debug(f"No NOTAM extracted for suffix: {suffix}")

            browser.close()
            logging.debug("Browser closed.")

        logging.info(f"Scraping complete. Found {len(results)} NOTAMs.")
        return results

    def _find_relevant_suffixes(self, page) -> List[str]:
        suffixes = []
        for img in page.query_selector_all("img[src*='plus.gif']"):
            try:
                div_id = img.evaluate("el => el.closest('div').id")
                suffix = div_id[len("divMainInfo_") :]  # noqa: E203
                logging.debug(f"Found div ID: {div_id}, suffix: {suffix}")

                msg_text = (
                    img.evaluate_handle(
                        "el => el.closest('tr').querySelector('#notamResult td.MsgText')"
                    )
                    .evaluate("el => el.innerText")
                    .strip()
                    .upper()
                )
                logging.debug(f"Message text for suffix {suffix}: {msg_text}")

                if "AD CLSD DUE WIP" in msg_text:
                    logging.debug(f"Suffix {suffix} is relevant.")
                    suffixes.append(suffix)
            except Exception as e:
                logging.warning(f"Error reading suffix: {e}")
        return suffixes

    def _extract_notam(self, page, suffix: str) -> NOTAM | None:
        try:
            img = page.query_selector(f"#divMainInfo_{suffix} img[src*='plus.gif']")
            if not img:
                logging.debug(f"No image found for suffix {suffix}")
                return None

            logging.debug(f"Clicking to expand NOTAM details for suffix {suffix}")
            img.click()
            page.wait_for_timeout(2000)

            expanded_div = page.query_selector(f"#divMoreInfo_{suffix}")
            if expanded_div:
                full_text = expanded_div.inner_text().upper()
                logging.debug(f"Full NOTAM text for suffix {suffix}:\n{full_text}")

                notam_id = re.search(r"NOTAM NO:\s*(\S+)", full_text)
                dates = re.search(r"B\)\s*(\d{10})\s*C\)\s*(\d{10})", full_text)

                if dates:
                    start_zulu = dates.group(1)
                    end_zulu = dates.group(2)
                    logging.debug(
                        f"Extracted dates - Start: {start_zulu}, End: {end_zulu}"
                    )

                    start_il = convert_zulu_to_israel(start_zulu).strftime(
                        "%Y-%m-%d %H:%M"
                    )
                    end_il = convert_zulu_to_israel(end_zulu).strftime("%Y-%m-%d %H:%M")
                    logging.debug(
                        f"Converted times - Start IL: {start_il}, End IL: {end_il}"
                    )

                    return {
                        "notam_id": notam_id.group(1) if notam_id else "UNKNOWN",
                        "start_il": start_il,
                        "end_il": end_il,
                    }
                else:
                    logging.debug(f"Dates not found in full text for suffix {suffix}")
        except Exception as e:
            logging.error(f"Error extracting NOTAM {suffix}: {e}")
        return None
