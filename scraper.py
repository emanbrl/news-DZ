import logging
import time
from datetime import datetime
from urllib.parse import urljoin

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
        #"category":
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

    logger.info(
        "Collected %d articles",
        len(articles)
    )

    for article in articles:
        print(article)


if __name__ == "__main__":
    main()