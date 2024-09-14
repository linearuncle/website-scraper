# 🕷️ Website Scraper

A powerful and flexible web scraping tool that allows you to download entire websites in various formats, including Markdown, PDF, and HTML.

## ✨ Features

- 🌐 Scrape entire websites starting from a given URL
- 💾 Save content in multiple formats: Markdown, PDF, and HTML
- ⚡ Concurrent scraping for improved performance
- 📁 Customizable output directory
- 🛠️ Built with asyncio and Playwright for efficient and robust scraping

## 📋 Requirements

- 🐍 Python 3.7+
- 🎭 Playwright
- 🍲 BeautifulSoup4
- ✍️ markdownify

## 🚀 Installation

### Cloning the Repository

1. Open a terminal or command prompt and run:
   ```
   git clone https://github.com/yourusername/website-scraper.git
   cd website-scraper
   ```

### Setting up a Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python projects or system-wide packages.

#### For macOS and Linux:

1. Create a virtual environment:
   ```
   python3 -m venv .venv
   ```

2. Activate the virtual environment:
   ```
   source .venv/bin/activate
   ```

#### For Windows:

1. Create a virtual environment:
   ```
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```
   .venv\Scripts\activate
   ```

### Installing Dependencies

Once your virtual environment is activated, install the required dependencies:

1. Install Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Install Playwright browsers:
   ```
   playwright install
   ```

## 🖥️ Usage

Run the scraper from the command line with the following syntax:

```
python src/main.py <start_url> [--formats FORMAT [FORMAT ...]] [--output OUTPUT_DIR] [--concurrency CONCURRENCY]
```

### 🔧 Arguments:

- `start_url`: The starting URL for scraping (required)
- `--formats`: Choose file formats to save (choices: markdown, pdf, html; default: markdown)
- `--output`: Specify output directory (optional)
- `--concurrency`: Number of concurrent crawling tasks (default: 10)

### 📝 Examples:

1. Scrape a website and save as Markdown (default):
   ```
   python src/main.py https://docs.firecrawl.dev/introduction
   ```

2. Scrape a website and save as both Markdown and PDF:
   ```
   python src/main.py https://python.langchain.com/v0.2/docs/introduction/ --formats markdown pdf
   ```

3. Scrape a website with custom output directory and concurrency, saving in all available formats:
   ```
   python src/main.py https://microsoft.github.io/autogen/docs/Getting-Started --formats markdown pdf html --output ./autogen_doc --concurrency 10
   ```

## 📂 Output

The scraped content will be saved in the `download` directory by default, organized by the website's name. You can specify a custom output directory using the `--output` argument.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements
- [OpenAI](https://openai.com/)
- [Cursor](https://www.cursor.com/)
- [Aider](https://aider.chat/)
- [markdownify](https://github.com/matthewwithanm/python-markdownify)

## 👤 Author

@LinearUncle - [X/Twitter](https://x.com/LinearUncle)

Project Link: [https://github.com/yourusername/website-scraper](https://github.com/yourusername/website-scraper)
