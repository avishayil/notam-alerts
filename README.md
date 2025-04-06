# ✈️ LLBG NOTAM Scraper & Notifier

This project scrapes NOTAMs (Notices to Airmen) from the Israeli Airports Authority website for LLBG (Ben Gurion Airport), detects relevant changes (e.g., **AD CLSD DUE WIP**), and sends updates via **Telegram notifications**.

---

## 🚀 Features

- Scrapes LLBG NOTAMs using Playwright
- Detects added, removed, or updated NOTAMs
- Converts NOTAM Zulu time to Israel local time
- Saves data locally in `notams.json`
- Sends Telegram alerts on changes
- Environment variables managed via `.env`

---

## 📁 Project Structure

```
notam_scraper/
├── src/                         # Source code folder
│   ├── constants.py             # Timezones, file paths
│   ├── data_handler.py          # Load/save/compare NOTAMs
│   ├── notifier.py              # Telegram or email notification sender
│   ├── scraper.py               # Web scraper for LLBG NOTAMs
│   ├── utils.py                 # Time conversion helpers
│   └── main.py                  # Entrypoint
├── tests/                       # Tests folder
├── main.py                      # Entrypoint
├── .env                         # Environment variables (excluded from git)
└── pyproject.toml               # Poetry-based dependency manager
```

---

## 📦 Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/)
- Telegram Bot & Channel

---

## 🛠️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-user/notam-alerts.git
cd notam-alerts
```

### 2. Install Poetry

If you don’t have Poetry installed:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. Install dependencies

```bash
poetry install
python -m playwright install
```

### 4. Set up environment variables

Create your own `.env` file:

```bash
cp .env.template .env
```

Then edit it and set the correct values:

```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHANNEL_ID=@your-channel-id-or-numeric-id
```

> ⚠️ Do not commit your `.env` file.

---

## ▶️ Usage

Run the scraper and notifier:

```bash
poetry run python main.py
```

---

## 📘 Example Telegram Message

```
🚨 LLBG NOTAM changes detected:

🟢 New or updated NOTAMs:
- L1234 from 2024-12-01 08:00 to 2024-12-01 18:00

🔴 Removed NOTAMs:
- L5678 from 2024-11-30 20:00 to 2024-12-01 06:00
```

---

## 🧪 Testing

You can test components interactively or run your tests with:

```bash
poetry run pytest
```

---

## 🧰 Development Tools

Includes support for:

- `black` (code formatting)
- `flake8` (linting)
- `isort` (import sorting)
- `pre-commit` hooks

Install hooks:

```bash
poetry run pre-commit install
```

Run lint:

```bash
poetry run pre-commit run --all-files
```

---

## 🤝 Contributing

Pull requests are welcome! Please open an issue to discuss any large changes or ideas first.

---

## 📄 License

MIT © 2025 Avishay Bar
