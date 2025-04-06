import logging
import os
from typing import Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


class NotamNotifier:
    def send(self, added: List[Dict], removed: List[Dict]) -> None:
        logging.debug("Preparing to send Telegram notification...")

        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
            logging.error("Missing Telegram credentials in environment variables.")
            return
        else:
            logging.debug(
                f"Using TELEGRAM_BOT_TOKEN: {'***' if TELEGRAM_BOT_TOKEN else 'None'}"
            )
            logging.debug(f"Using TELEGRAM_CHANNEL_ID: {TELEGRAM_CHANNEL_ID}")

        body = self._compose_message(added, removed)
        if not body:
            logging.debug("No changes to notify. Skipping Telegram message.")
            return

        try:
            telegram_url = (
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            )
            payload = {
                "chat_id": TELEGRAM_CHANNEL_ID,
                "text": body,
                "parse_mode": "Markdown",
            }
            logging.debug(f"Sending payload to Telegram: {payload}")
            response = requests.post(telegram_url, json=payload)

            if response.status_code != 200:
                logging.error(
                    f"Telegram API error ({response.status_code}): {response.text}"
                )
            else:
                logging.info("Notification sent successfully.")
        except Exception as e:
            logging.error(f"Error sending Telegram notification: {e}")

    def _compose_message(self, added, removed) -> str:
        logging.debug(
            f"Composing message for {len(added)} added and {len(removed)} removed NOTAMs."
        )
        if not added and not removed:
            return ""

        msg = "🚨 *LLBG NOTAM changes detected:*\n\n"
        if added:
            msg += "🟢 *New or updated NOTAMs:*\n"
            for n in added:
                logging.debug(f"Added NOTAM: {n}")
                msg += f"- `{n['notam_id']}` from {n['start_il']} to {n['end_il']}\n"
        if removed:
            msg += "\n🔴 *Removed NOTAMs:*\n"
            for n in removed:
                logging.debug(f"Removed NOTAM: {n}")
                msg += f"- `{n['notam_id']}` from {n['start_il']} to {n['end_il']}\n"
        return msg
