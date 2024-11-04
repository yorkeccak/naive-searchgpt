# Naive SearchGPT

A rather "naive" implementation of how AI-powered search engines might work. After [ChatGPT Search](https://openai.com/index/introducing-chatgpt-search/) released just a few days ago, I noticed that the search results are literally just the top few bing search results - so I thought, that doesn't sound that hard. 2 hrs later, here we are. This project demonstrates a basic approach to how systems like SearchGPT might work, by crawling web content and using gpt-4o to generate coherent summaries with source attribution and links back to the original content.

## Overview

This script:
1. Searches Bing for your query
2. Crawls the top results (respecting robots.txt)
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
python news.py --query "AI developments"
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
╭────────────────────────────────────────────────────────────╮
│ 🔍 Fetching news about: who is going to win us election... │
╰────────────────────────────────────────────────────────────╯
📋 Found Articles
├── • US election 2024 results: When will we know who won?
├── • Who Is Favored To Win The 2024 Presidential Election?
├── • US election polls: Who is ahead - Harris or Trump? - BBC
├── • Harris v Trump: 2024 presidential election prediction model
└── • Who will win the US election? Our experts’ final predictions

Skipping https://www.economist.com/interactive/us-2024-election/prediction-model/president (blocked by robots.txt)
╭──────────────────────────╮
│ 🤖 Generating summary... │
╰──────────────────────────╯

📰 Who Will Win the US Presidential Election 2024?

US election 2024 results: When will we know who won?                                  

 • The election process on November 5 may not immediately yield a clear winner due to potential close races and        
   recounts.                                                                                                           
 • Key swing states like Pennsylvania, Michigan, and Arizona are crucial and their results may finalize the election   
   outcome.                                                                                                            
 • Recent changes in election administration, and fewer mail-in votes compared to 2020, could lead to quicker results. 
 • The election could still be prolonged, as in the past, where final outcomes were declared days or weeks later.      

Source: BBC News   

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
