# Telegram Markdown Bot 🤖

A powerful Telegram bot that converts text, HTML, and URLs to beautifully formatted markdown. Perfect for developers, writers, and anyone who works with markdown formatting.

## ✨ Features

- 📝 **Text to Markdown**: Convert plain text to markdown format
- 🌐 **URL Processing**: Fetch and convert web pages to markdown
- 🔗 **Smart Link Handling**: Convert HTML links to markdown format
- 🏷️ **Keyword Mapping**: Replace predefined keywords with their corresponding URLs
- 📄 **File Output**: Get results as downloadable markdown files
- 🎨 **HTML Support**: Convert HTML content to clean markdown

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- A Telegram Bot Token (get one from [@BotFather](https://t.me/botfather))

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/markdown-bot.git
   cd markdown-bot
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:

   ```env
   YOUR_BOT_TOKEN=your_telegram_bot_token_here
   ```

5. **Configure keywords (optional)**
   
   Edit `keywords.json` to add your custom keyword-to-URL mappings:

   ```json
   {
     "Google": "https://www.google.com/",
     "YouTube": "https://www.youtube.com/",
     "GitHub": "https://github.com/",
     "YourKeyword": "https://your-url.com/"
   }
   ```

6. **Run the bot**

   ```bash
   python markdown_bot.py
   ```

## 🔧 Usage

### Basic Commands

- Send any text to convert it to markdown format
- Send a URL to fetch and convert the webpage to markdown
- Use keywords from your `keywords.json` to auto-replace them with links

### Examples

**Text Input:**

```text
Hello World! Visit Google for search.
```

**Bot Output:**

```markdown
Hello World! Visit [Google](https://www.google.com/) for search.
```

**URL Input:**

```text
https://example.com
```

**Bot Output:**

- Fetches the webpage content
- Converts it to clean markdown
- Sends it as a downloadable `.md` file

## 📁 Project Structure

```text
markdown-bot/
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore file
├── Dockerfile          # Docker configuration
├── keywords.json       # Keyword-to-URL mappings
├── markdown_bot.py     # Main bot script
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── START.md           # Setup instructions
```

## 🐳 Docker Support

You can also run the bot using Docker:

1. **Build the image**

   ```bash
   docker build -t markdown-bot .
   ```

2. **Run the container**

   ```bash
   docker run -d --name markdown-bot --env-file .env markdown-bot
   ```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `YOUR_BOT_TOKEN` | Telegram Bot Token from BotFather | Yes |

### Keywords Configuration

The `keywords.json` file allows you to define custom mappings that the bot will automatically convert:

```json
{
  "keyword1": "https://example1.com",
  "keyword2": "https://example2.com"
}
```

When users send text containing these keywords, they'll be automatically converted to markdown links.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔧 Development

### Setting up development environment

```bash
# Clone the repo
git clone https://github.com/your-username/markdown-bot.git
cd markdown-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your bot token
echo "YOUR_BOT_TOKEN=your_token_here" > .env

# Run the bot
python markdown_bot.py
```

### Dependencies

- `python-telegram-bot` - Telegram Bot API wrapper
- `python-dotenv` - Environment variable management
- `markdown` - Markdown processing
- `markdownify` - HTML to Markdown conversion
- `beautifulsoup4` - HTML parsing

## 📞 Support

If you have any questions or run into issues:

1. Check the [Issues](https://github.com/your-username/markdown-bot/issues) page
2. Create a new issue if your problem isn't already reported
3. Include as much detail as possible about your setup and the issue

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

---

Made with ❤️ for the Telegram community
