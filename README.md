# Naive SearchGPT

A simple implementation exploring the concept behind AI-powered search engines. This project demonstrates a basic approach to how systems like SearchGPT might work, by crawling web content and using AI to generate coherent summaries.

## Overview

This script:
1. Searches Bing for your query
2. Scrapes the top results (respecting robots.txt)
3. Uses GPT-4 to analyze and summarize the articles
4. Presents a clean, formatted summary with source attribution

The output is specifically tailored for news-style responses, providing:
- Key bullet points summarizing main developments
- Source citations and links
- Structured, easy-to-read format

## Requirements

- Python 3.8+
- OpenAI API key
- Required Python packages (install via `pip install -r requirements.txt`):
  - requests
  - beautifulsoup4
  - openai
  - python-dotenv
  - rich

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yorkeccak/naive-searchgpt.git
cd naive-searchgpt
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

Basic usage with default parameters (5 articles about tech news):
```bash
python news.py
```

Search for specific topics:
```bash
python news.py --query "who is going to win us election"
python news.py --query "latest AI developments"
python news.py --query "climate change solutions"
```

Specify number of articles to analyze:
```bash
python news.py --query "cryptocurrency trends" --articles 3
```

## Command Line Arguments

- `--query`: The search query (default: "latest tech news")
- `--articles`: Number of articles to analyze (default: 5)

## Example Output

```
📋 Found Articles
├── Biden vs Trump: Latest Polls and Predictions for 2024
├── Analysis: Key Battleground States in Presidential Race
└── Electoral College Projections for November

🤖 Generating summary...

📰 2024 US Presidential Election Overview

### Current State of the Presidential Race

* Recent polls show a tight race between incumbent Joe Biden and Donald Trump
* Key battleground states like Pennsylvania, Michigan, and Georgia remain crucial
* Economic factors and voter turnout expected to play decisive roles
* Both campaigns focusing on swing voters and demographic shifts

*Source: [Political Analysis Weekly](https://example.com/analysis)*

...
```

## Limitations

- Basic web scraping might not work on all news sites
- Respects robots.txt but might still be blocked by some sites
- Limited by OpenAI API rate limits and costs
- Results quality depends on search engine results and GPT-4's interpretation
- Queries with time elements (e.g., "Today's news", "Latest developments") may fail due to web scraping limitations
- Currently uses web scraping instead of Bing API (API integration planned for future release)

## Contributing

Feel free to open issues or submit pull requests with improvements!

## License

MIT License - See LICENSE file for details

## Disclaimer

This is an educational project demonstrating basic concepts. For production use, consider rate limiting, caching, and proper error handling. Always respect websites' terms of service and robots.txt when scraping.
```

You might also want to create a `requirements.txt` file:

```text:requirements.txt
requests>=2.31.0
beautifulsoup4>=4.12.0
openai>=1.3.0
python-dotenv>=1.0.0
rich>=13.7.0