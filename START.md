## 1. Activate the Virtual Environment

```bash
source venv/bin/activate
```

## 2. Install python-telegram-bot Package

```bash
pip install python-telegram-bot --upgrade
pip install python-dotenv
pip install markdown
pip install markdownify
pip install beautifulsoup4
```

## 3. Run it:

```bash
python markdown_bot.py
```

## 4. Summary of Commands:

```bash
mkdir telegram_bot
cd telegram_bot
python3 -m venv venv
source venv/bin/activate       # or venv\Scripts\activate on Windows
```

## 5. Build and run:

```bash
docker build -t markdown-bot .
docker run -d --env-file .env --name markdown-bot markdown-bot
```
