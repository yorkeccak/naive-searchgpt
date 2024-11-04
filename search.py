import requests
from bs4 import BeautifulSoup
import urllib.robotparser
from openai import OpenAI
import os, json
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.tree import Tree
import argparse
from dotenv import load_dotenv

# Initialize Rich console for better formatting
console = Console()

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

def can_fetch(url):
    """Check if we're allowed to fetch the URL according to robots.txt"""
    try:
        rp = urllib.robotparser.RobotFileParser()
        parsed_url = urllib.parse.urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch("*", url)
    except Exception:
        # If there's any error checking robots.txt, err on the side of caution
        return False

def fetch_news(query="latest tech news", num_articles=5):
    console.print(Panel.fit(f"🔍 Fetching news about: {query}...", style="bold blue"))
    
    # Update search URL with custom query
    BING_URL = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    
    try:
        response = requests.get(BING_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        console.print(f"[bold red]Failed to fetch search results: {str(e)}[/bold red]")
        return

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Define lists to store article data
    titles = []
    links = []
    full_articles = []
    
    # Find all result items and extract specified number of relevant items
    articles = soup.find_all("li", class_="b_algo")[:num_articles]
    
    # Create a tree for collapsible view
    article_tree = Tree("📋 [bold]Found Articles[/bold]")
    for article in articles:
        title_element = article.find("h2")
        if title_element:
            article_tree.add(f"[dim]• {title_element.get_text().strip()}[/dim]")
    console.print(article_tree)
    console.print()
    
    with console.status(f"[bold green]Analyzing {num_articles} articles...") as status:
        for i, article in enumerate(articles, 1):
            title_element = article.find("h2")
            if title_element:
                title = title_element.get_text().strip()
                link = title_element.find("a")["href"]
                
                status.update(f"[bold green]Processing article {i}/{num_articles}...")
                
                # Always check robots.txt for individual article websites
                if not can_fetch(link):
                    console.print(f"[yellow]Skipping {link} (blocked by robots.txt)[/yellow]")
                    continue
                
                try:
                    article_response = requests.get(link, timeout=10)
                    article_response.raise_for_status()
                    article_soup = BeautifulSoup(article_response.text, "html.parser")
                    
                    paragraphs = article_soup.find_all("p")
                    full_text = "\n".join([p.get_text().strip() for p in paragraphs])[:5000]
                    
                    titles.append(title)
                    links.append(link)
                    full_articles.append(full_text)
                    
                except requests.RequestException:
                    continue

    if not titles:
        console.print("[bold red]No articles found![/bold red]")
        return

    # Create context for OpenAI
    context = "\n".join([f"Title: {titles[i]}\nContent: {full_articles[i]}\nLink: {links[i]}" 
                        for i in range(len(titles))])
    
    console.print(Panel.fit("🤖 Generating summary...", style="bold yellow"))

    # Updated OpenAI call with proper model and schema
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",  # Use the latest model that supports structured output
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "news_summary_schema",  # Required name field
                "description": "A schema for news article summaries",  # Optional but recommended
                "strict": True,  # Enable strict mode for reliable output
                "schema": {  # Wrap the schema definition in a schema field
                    "type": "object",
                    "properties": {
                        "news_summary": {
                            "type": "object",
                            "properties": {
                                "topic": {"type": "string"},
                                "articles": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "headline": {"type": "string"},
                                            "key_points": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            },
                                            "source": {
                                                "type": "object",
                                                "properties": {
                                                    "title": {"type": "string"},
                                                    "url": {"type": "string"}
                                                },
                                                "required": ["title", "url"],
                                                "additionalProperties": False
                                            }
                                        },
                                        "required": ["headline", "key_points", "source"],
                                        "additionalProperties": False
                                    }
                                }
                            },
                            "required": ["topic", "articles"],
                            "additionalProperties": False
                        }
                    },
                    "required": ["news_summary"],
                    "additionalProperties": False
                }
            }
        },
        messages=[
            {
                "role": "system",
                "content": "You are a news summarizer that provides concise, accurate summaries with proper source attribution."
            },
            {
                "role": "user",
                "content": f"Analyze and summarize these articles about '{query}' into their key points but not cutting out details:\n\n{context}"
            }
        ]
    )

    try:
        # Parse the JSON response
        summary_data = json.loads(completion.choices[0].message.content)
        
        # Format and display the output
        console.print(f"\n[bold blue]📰 {summary_data['news_summary']['topic']}[/bold blue]\n")
        
        for article in summary_data['news_summary']['articles']:
            # Create markdown formatted output
            headline = f"### {article['headline']}\n\n"
            
            # Format key points with proper spacing
            points = "\n".join([f"* {point}\n" for point in article['key_points']])
            points += "\n"
            
            source = f"*Source: [{article['source']['title']}]({article['source']['url']})*\n"
            
            # Use proper markdown formatting
            markdown_content = headline + points + source
            console.print(Markdown(markdown_content))
            console.print("---")

    except json.JSONDecodeError:
        console.print("[bold red]Error: Invalid JSON response from AI[/bold red]")
        if hasattr(completion.choices[0].message, 'content'):
            console.print(f"Raw response: {completion.choices[0].message.content}")
    except KeyError as e:
        console.print(f"[bold red]Error: Missing expected field in response: {str(e)}[/bold red]")
        console.print(f"Received structure: {json.dumps(summary_data, indent=2)}")
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {str(e)}[/bold red]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch and summarize news articles.')
    parser.add_argument('--query', type=str, default='latest tech news',
                      help='The search query for news articles')
    parser.add_argument('--articles', type=int, default=5,
                      help='Number of articles to analyze (default: 5)')
    
    args = parser.parse_args()
    
    try:
        fetch_news(args.query, args.articles)
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")