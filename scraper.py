import logging
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse
import json

import requests
from bs4 import BeautifulSoup


# =========================================
# Configuration
# =========================================

BASE_URL = "https://www.aps.dz"
SOURCE_URL = f"{BASE_URL}/en"


REQUEST_TIMEOUT = 10
REQUEST_DELAY = 1


# =========================================
# Logging
# =========================================

logging.basicConfig(
    level = logging.INFO,
    format = "%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)


# =========================================
# HTTP session
# =========================================

session = requests.Session()

session.headers.update({
    "User-Agent": "News-DZ/1.0"
})


# =========================================
# Fetch page
# =========================================

def fetch_page(url):
    """Fetch a webpage and return its HTML"""

    response = session.get(
        url,
        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()

    return response.text


# =========================================
# Parse article
# =========================================

def get_category(article_url):
    """Extract the category from an APS article URL."""

    path_parts = urlparse(article_url).path.strip("/").split("/")

    if len(path_parts) >= 2:
        return path_parts[-2]

    return None

def parse_article(article_url):

    """Extract article metadata from an APS article page."""

    html = fetch_page(article_url)

    article_soup = BeautifulSoup(
        html,
        "html.parser"
    )

    title = article_soup.find("h1")
    date = article_soup.find("span", class_="text-xs")
    lead = article_soup.find("p") 
    category = get_category(article_url)

    description = (
        lead.get_text(" ", strip=True)
        if lead
        else None
    )

    date_text = (
        date.get_text(strip=True)
        if date
        else None
    )

    published_at = None

    if date_text:
        published_at = datetime.strptime(
            date_text,
            "%A, %B %d, %Y %H:%M"
        )

    
    article = {
        "source":"APS",
        "title": (
            title.get_text(strip=True)
            if title
            else None
        ),
        "url": article_url,
        "category": category,
        "published_at": published_at,
        "description": description
    }

    return article


# =========================================
# Find article URLs
# =========================================

def get_article_urls(soup):
    """Find unique article URLs on the APS homepage."""

    article_urls = set()

    for link in soup.find_all("a"):
        image = link.find("img")

        if image:
            src = image.get("src")

            if src and "image%2Farticle" in src:
                article_urls.add(link.get("href"))

    return article_urls


def save_articles(articles,filepath):
    """Save articles to a JSON file."""
    
    json_articles = [
        {
            **article,
            "published_at": (
                article["published_at"].isoformat()
                if article["published_at"]
                else None
            ),
        }
        for article in articles
    ]

    with open(
        filepath,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            json_articles,
            file,
            ensure_ascii=False,
            indent=2,
        )

# =========================================
# Main scraper
# =========================================

def main():

    html = fetch_page(SOURCE_URL)

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    article_urls = get_article_urls(soup)

    logger.info(
        "Found %d unique articles",
        len(article_urls),
    )

    articles = []

    for article_path in article_urls:

        article_url = urljoin(
            BASE_URL,
            article_path,
        )

        try:
            article = parse_article(article_url)

            if article:
                articles.append(article)

        except requests.RequestException as error:
            logger.error(
                "Failed to fetch %s: %s",
                article_url,
                error,
            )

        time.sleep(REQUEST_DELAY)

    articles.sort(
        key=lambda article: article["published_at"] or datetime.min,
        reverse=True,
    )
    
    logger.info(
        "Collected %d articles",
        len(articles)
    )

    save_articles(
        articles,
        "data/aps_articles.json",
    )

    logger.info(
        "Saved dataset to data/aps_articles.json"
    )

if __name__ == "__main__":
    main()