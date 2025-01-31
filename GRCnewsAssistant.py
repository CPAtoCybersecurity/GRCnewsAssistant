#!/usr/bin/env python3
# GRCnewsAssistant.py
# Consolidated GRC News Assistant with AI Analysis

import csv
import requests
import datetime
import time
import logging
import json
import tempfile
import os
import subprocess
import platform
import sys
import urllib.parse
from newspaper import Article
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_api_key() -> str:
    """Get NewsData.io API key from environment variable."""
    api_key = os.getenv('NEWSDATA_API_KEY')
    if not api_key:
        logger.error("""
NewsData.io API key not found!

Please set your API key as an environment variable:

For macOS/Linux:
    export NEWSDATA_API_KEY='your_api_key_here'

For Windows (Command Prompt):
    set NEWSDATA_API_KEY=your_api_key_here

For Windows (PowerShell):
    $env:NEWSDATA_API_KEY='your_api_key_here'

You can add this to your shell's startup file (.bashrc, .zshrc, etc.) 
to make it permanent.
""")
        sys.exit(1)
    return api_key

def get_clipboard_command() -> List[str]:
    """Get the appropriate clipboard command based on OS."""
    system = platform.system().lower()
    
    if system == 'darwin':  # macOS
        return ['pbpaste']
    elif system == 'linux':
        # Check if xclip is installed
        try:
            subprocess.run(['xclip', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return ['xclip', '-selection', 'clipboard', '-o']
        except FileNotFoundError:
            logger.error("""
xclip not found! On Linux, please install xclip:

For Ubuntu/Debian:
    sudo apt-get install xclip

For Fedora:
    sudo dnf install xclip

For other distributions, use your package manager to install xclip.
""")
            sys.exit(1)
    elif system == 'windows':
        return ['powershell.exe', '-command', 'Get-Clipboard']
    else:
        logger.error(f"Unsupported operating system: {system}")
        sys.exit(1)

def read_keywords(filename: str = "keywords.csv") -> List[str]:
    """Read and decode keywords from CSV file."""
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            return [urllib.parse.unquote(row[0]) for row in reader]
    except Exception as e:
        logger.error(f"Error reading keywords file: {e}")
        return []

def search_news(keyword: str, api_key: str, category: str = "technology", language: str = "en") -> List[Dict]:
    """Search NewsData.io API for articles matching keyword."""
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={keyword}&language={language}&category={category}"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["status"] == "success":
            articles = []
            for article in data["results"]:
                articles.append({
                    "date": datetime.date.today().strftime("%Y-%m-%d"),
                    "keyword": keyword,
                    "headline": article["title"],
                    "description": article["description"],
                    "url": article["link"]
                })
            return articles
        else:
            logger.error(f"API request failed: {data.get('results', 'No error message')}")
            return []
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return []

def save_to_csv(articles: List[Dict], filename: str = "grcdata.csv"):
    """Save articles to CSV file."""
    try:
        # Ensure file exists with header
        if not os.path.exists(filename):
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['date', 'keyword', 'title', 'description', 'url'])
        
        # Append valid articles
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for article in articles:
                if article and all(article.get(key) for key in ["date", "keyword", "headline", "description", "url"]):
                    writer.writerow([
                        article["date"],
                        article["keyword"],
                        article["headline"],
                        article["description"],
                        article["url"]
                    ])
    except Exception as e:
        logger.error(f"Error writing to {filename}: {e}")

def save_urls(articles: List[Dict], filename: str = "urls.csv"):
    """Save URLs to separate CSV file."""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Only write valid URLs
            for article in articles:
                if article and article.get("url"):
                    writer.writerow([article["url"]])
    except Exception as e:
        logger.error(f"Error writing URLs to {filename}: {e}")

def extract_article_content(url: str) -> Dict:
    """Extract article content using newspaper4k."""
    article = Article(url, fetch_images=False)
    try:
        article.download()
        article.parse()
        article.nlp()
        
        return {
            "title": article.title or "Not Found",
            "keywords": article.keywords if article.keywords else [],
            "authors": article.authors if article.authors else ["Not Found"],
            "summary": article.summary or "Not Found",
            "text": article.text or "Not Found",
            "publish_date": article.publish_date.isoformat() if article.publish_date else "Not Found",
            "url": url
        }
    except Exception as e:
        logger.error(f"Failed to process article from {url}: {e}")
        return None

def analyze_with_fabric(content: Dict) -> Dict:
    """Process article content with fabric label_and_rate."""
    try:
        # Create temporary file with formatted content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            formatted_content = (
                f"Title: {content['title']}\n"
                f"Authors: {', '.join(content['authors'])}\n"
                f"Keywords: {', '.join(content['keywords'])}\n"
                f"Summary: {content['summary']}\n"
                f"URL: {content['url']}\n"
            )
            temp_file.write(formatted_content)
            temp_file_path = temp_file.name

        # Copy content to clipboard using OS-specific command
        with open(temp_file_path, 'r') as f:
            subprocess.run(['pbcopy' if platform.system() == 'Darwin' else 'clip'], 
                         input=f.read().encode(), 
                         check=True)
        
        # Create temporary output file for fabric results
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as output_file:
            output_path = output_file.name
        
        # Run fabric command with OS-specific clipboard command
        clipboard_cmd = get_clipboard_command()
        cmd = f'{" ".join(clipboard_cmd)} | fabric -p label_and_rate -o "{output_path}"'
        subprocess.run(cmd, shell=True, timeout=15, check=True)
        
        # Read fabric results
        with open(output_path, 'r') as f:
            fabric_data = json.loads(f.read())
        
        # Cleanup temporary files
        os.unlink(temp_file_path)
        os.unlink(output_path)
        
        return fabric_data
    except Exception as e:
        logger.error(f"Error in fabric analysis: {e}")
        return None

def create_rated_csv(articles: List[Dict], analysis_results: List[Dict]):
    """Create grcdata_rated.csv with fabric analysis results."""
    try:
        # Create new file with analyzed data
        with open('grcdata_rated.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            header = [
                'date', 'keyword', 'title', 'description', 'url',
                'one-sentence-summary', 'labels', 'rating',
                'rating-explanation', 'quality-score', 'quality-score-explanation'
            ]
            writer.writerow(header)
            
            # Write data with analysis
            for article, analysis in zip(articles, analysis_results):
                if article and article.get('url'):  # Ensure article data is valid
                    if analysis:
                        writer.writerow([
                            article['date'],
                            article['keyword'],
                            article['headline'],
                            article['description'],
                            article['url'],
                            analysis.get('one-sentence-summary', ''),
                            analysis.get('labels', ''),
                            analysis.get('rating', ''),
                            '; '.join(analysis.get('rating-explanation', [])),
                            str(analysis.get('quality-score', '')),
                            '; '.join(analysis.get('quality-score-explanation', []))
                        ])
                    else:
                        # Write without analysis if it failed, but still include article data
                        writer.writerow([
                            article['date'],
                            article['keyword'],
                            article['headline'],
                            article['description'],
                            article['url'],
                            '', '', '', '', '', ''
                        ])
    except Exception as e:
        logger.error(f"Error updating grcdata.csv with analysis: {e}")

def main():
    """Main execution flow."""
    logger.info("Starting GRC News Assistant")
    
    # Get API key from environment variable
    api_key = get_api_key()
    
    # Read keywords
    keywords = read_keywords()
    if not keywords:
        logger.error("No keywords found in keywords.csv")
        return
    
    # Collect articles
    all_articles = []
    for keyword in keywords:
        logger.info(f"Searching for articles about: {keyword}")
        articles = search_news(keyword.strip(), api_key)
        if articles:
            all_articles.extend(articles)
            logger.info(f"Found {len(articles)} articles for '{keyword}'")
        else:
            logger.warning(f"No articles found for '{keyword}'")
    
    if not all_articles:
        logger.error("No articles found for any keywords")
        return
    
    # Save initial results
    save_to_csv(all_articles)
    save_urls(all_articles)
    logger.info(f"Saved {len(all_articles)} articles to CSV files")
    
    # Process articles with newspaper4k and fabric
    logger.info("Processing articles with newspaper4k and fabric")
    analysis_results = []
    
    for article in all_articles:
        url = article["url"]
        logger.info(f"Processing: {url}")
        
        # Extract content
        content = extract_article_content(url)
        if content:
            # Analyze with fabric
            analysis = analyze_with_fabric(content)
            analysis_results.append(analysis)
        else:
            analysis_results.append(None)
    
    # Create rated CSV with analysis results
    create_rated_csv(all_articles, analysis_results)
    logger.info("Completed processing with AI analysis. Results saved to grcdata.csv and grcdata_rated.csv")

if __name__ == "__main__":
    main()
