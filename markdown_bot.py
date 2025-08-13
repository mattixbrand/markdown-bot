from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler,
    ContextTypes, filters
)
from telegram.constants import ParseMode
import logging
import io
import os
import re
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_md
import markdown

# Load .env file
load_dotenv()
BOT_TOKEN = os.getenv("YOUR_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Regex patterns
MARKDOWN_LINK_RE = re.compile(r'\[([^\]]+)\]\((https?://[^\)]+)\)')
HTML_TAG_RE = re.compile(r'<[^>]+>')
URL_RE = re.compile(r'(https?://\S+)')

# Load label→URL map from keywords.json
def load_label_map():
    try:
        with open("keywords.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("keywords.json not found, returning empty map")
        return {}

label_to_url = load_label_map()

# Utility functions
def extract_known_labels(text):
    return [label for label in label_to_url if label in text]

def contains_only_labels(text):
    words = re.split(r"\s+", text.strip())
    return all(word in label_to_url for word in words if word)

def extract_markdown_links(text):
    return MARKDOWN_LINK_RE.findall(text)

def normalize_markdown(text):
    markdown_links = dict(extract_markdown_links(text))
    placeholder_map = {}
    protected_text = text

    for i, (label, url) in enumerate(markdown_links.items()):
        placeholder = f"__LINK_PLACEHOLDER_{i}__"
        placeholder_map[placeholder] = f"[{label}]({url})"
        protected_text = protected_text.replace(f"[{label}]({url})", placeholder)

    for placeholder, original_md_link in placeholder_map.items():
        protected_text = protected_text.replace(placeholder, original_md_link)

    return protected_text.strip()

# Conversion functions
def convert_to_mdx(md_text):
    return md_text

def convert_to_html(md_text):
    return markdown.markdown(md_text)

async def send_all_formats(msg, markdown_text, header_msg):
    mdx_text = convert_to_mdx(markdown_text)
    html_text = convert_to_html(markdown_text)

    preview = "\n".join(markdown_text.splitlines()[:10]) or "…"
    await msg.reply_text(f"{header_msg}:\n{preview}")

    files = {
        "response.md": markdown_text,
        "response.mdx": mdx_text,
        "response.html": html_text
    }

    for fname, content in files.items():
        buf = io.StringIO(content)
        buf.name = fname
        await msg.reply_document(InputFile(buf))

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Hello!*\n\n"
        "Send me *Telegram-formatted text*, *Markdown*, or upload `.md` / `.mdx` / `.html` files.\n\n"
        "I'll process and return normalized files in three formats:\n"
        "📄 `response.md`\n"
        "📄 `response.mdx`\n"
        "📄 `response.html`\n\n"
        "*Supports:*\n"
        "- Telegram links and entities\n"
        "- Markdown text and links\n"
        "- Keywords from `keywords.json`\n"
        "- File uploads (`.md`, `.mdx`, `.html`)\n\n"
        "✅ Try sending:\n"
        "`You can copy it by command+C and try to test it its result will be [Telegram Bot API](https://core.telegram.org/bots/api):` [Telegram Bot API](https://core.telegram.org/bots/api)\n"
        "---\n"
        "👋 *您好！*\n\n"
        "请发送 *Telegram 格式的文本*、Markdown 文本，或上传 `.md` / `.mdx` / `.html` 文件。\n\n"
        "我将处理并返回以下三种格式的规范化文件：\n"
        "📄 `response.md`\n"
        "📄 `response.mdx`\n"
        "📄 `response.html`\n\n"
        "*支持：*\n"
        "- Telegram 链接和实体\n"
        "- Markdown 文本和链接\n"
        "- 来自 `keywords.json` 的关键字\n"
        "- 文件上传（`.md`, `.mdx`, `.html`）\n\n"
        "✅ 例如尝试发送：\n"
        "`您可以通过 command+C 复制它并尝试测试它，其结果将是 [Telegram Bot API](https://core.telegram.org/bots/api):` [Telegram Bot API](https://core.telegram.org/bots/api)\n"
        "或者上传 Markdown/HTML 文件！",
        parse_mode=ParseMode.MARKDOWN
    )

# Text message handler
async def process_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    text = msg.text or msg.caption or ""
    entities = msg.entities or []

    if not text.strip():
        await msg.reply_text("❌ No text detected.")
        return

    # Priority 1: Markdown-style links
    markdown_links = extract_markdown_links(text)
    if markdown_links:
        markdown_text = "\n".join(f"[{label}]({url})" for label, url in markdown_links)
        normalized = normalize_markdown(markdown_text)
        await send_all_formats(msg, normalized, "✅ Received Markdown Links")
        return

    # Priority 2: Raw HTML, Markdown-ish text, or Telegram entities
    if HTML_TAG_RE.search(text) or "#" in text or "-" in text or entities:
        markdown_text = text
        # Replace Telegram entity text with Markdown links
        for entity in sorted(entities, key=lambda e: e.offset, reverse=True):
            if entity.type == "text_link":
                linked_text = text[entity.offset: entity.offset + entity.length]
                markdown_link = f"[{linked_text}]({entity.url})"
                markdown_text = (
                    markdown_text[:entity.offset] +
                    markdown_link +
                    markdown_text[entity.offset + entity.length:]
                )

        # Replace keywords with Markdown links
        for keyword, url in label_to_url.items():
            # Use word boundaries to avoid partial matches
            markdown_text = re.sub(
                r'\b' + re.escape(keyword) + r'\b',
                f'[{keyword}]({url})',
                markdown_text
            )

        normalized = normalize_markdown(markdown_text)
        await send_all_formats(msg, normalized, "✅ Raw Markdown, HTML, or Telegram Links Detected")
        return

    # Priority 3: Only known keywords
    if contains_only_labels(text):
        markdown_text = "\n".join(f"[{label}]({label_to_url[label]})" for label in extract_known_labels(text))
        normalized = normalize_markdown(markdown_text)
        await send_all_formats(msg, normalized, "✅ Markdown Links Generated from Keywords")
        return

    # Priority 4: Mixed text and known labels
    labels = extract_known_labels(text)
    if labels:
        lines = text.strip().splitlines()
        markdown_lines = []

        for line in lines:
            if contains_only_labels(line):
                markdown_lines.extend([
                    f"[{label}]({label_to_url[label]})" for label in extract_known_labels(line)
                ])
            else:
                markdown_lines.append(line)

        markdown_text = "\n".join(markdown_lines)
        normalized = normalize_markdown(markdown_text)
        await send_all_formats(msg, normalized, "✅ Mixed Markdown + Keywords")
        return

    # Priority 5: Fallback for no valid content
    await msg.reply_text("❌ No valid markdown, keywords, or links found.")

# File upload handler
async def process_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    file = msg.document or msg.effective_attachment
    filename = file.file_name.lower()

    if not (filename.endswith(".md") or filename.endswith(".mdx") or filename.endswith(".html")):
        await msg.reply_text("❌ Only .md, .mdx, and .html files are supported.")
        return

    file_obj = await file.get_file()
    content = (await file_obj.download_as_bytearray()).decode("utf-8")

    if filename.endswith(".html"):
        content = html_to_md(content)

    normalized = normalize_markdown(content)
    await send_all_formats(msg, normalized, "✅ Processed Uploaded File")

# Startup log
async def on_startup(app):
    logger.info("✅ Bot started and connected to Telegram.")
    print("✅ Bot is running and ready!")

# Entry point
if __name__ == "__main__":
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN not found in .env")

    app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", start_command))
    app.add_handler(MessageHandler(filters.TEXT | filters.CAPTION | filters.FORWARDED, process_text))
    app.add_handler(MessageHandler(filters.Document.ALL, process_file))
    app.run_polling()