import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import logging
from datetime import datetime

BASE_URL = "https://www.aps.dz"
SOURCE_URL = f"{BASE_URL}/en"

session = requests.Session()

session.headers.update({
    "User-Agent": "News-DZ/1.0"
})


logging.basicConfig(
    level = logging.INFO,
    format = "%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)


# =========================================
# Parse on article
# =========================================

def parse_article(article_url):

    html = fetch_page(article_url)

    # Parse homepage HTML
    article_soup = BeautifulSoup(
        html,
        "html.parser"
    )

    title = article_soup.find("h1")
    date = article_soup.find("span", class_="text-xs")
    lead = article_soup.find("p")
    #source = 
    #category = 

    description = lead.get_text(" ", strip=True) if lead else None

    date_text = date.get_text(strip=True) if date else None

    published_at = None

    if date_text:
        published_at = datetime.strptime(
            date_text,
            "%A, %B %d, %Y %H:%M"
        )
        
    article = {
        "title": title.get_text(strip=True) if title else None,
        "url": article_url,
        "date": published_at,
        "description": description
        #"source":
        #"category":
    }

    return article


# =========================================
# Find article URLs
# =========================================
def get_article_urls(soup):

    article_urls = set()

    for link in soup.find_all("a"):
        image = link.find("img")

        if image:
            src = image.get("src")

            if "image%2Farticle" in src:
                article_urls.add(link.get("href"))

    return article_urls


# =========================================
# Fetch homepage
# =========================================

def fetch_page(url):
    response = session.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    return response.text

html = fetch_page(SOURCE_URL)

soup = BeautifulSoup(
    html, 
    "html.parser"
)


# =========================================
# Find article URLs
# =========================================

article_urls = get_article_urls(soup)

logger.info(
    "Found %d unique articles",
    len(article_urls)
)
# =========================================
# Parse articles
# =========================================

articles = []

for article_path in article_urls:

    article_url = urljoin(BASE_URL, article_path)

    try:
        article = parse_article(article_url)

        if article:
            articles.append(article)

    except requests.RequestsException as error:
        logger.error(
            "Failed to fetch %s: %s",
            article_url,
            error
        )

    time.sleep(1)

logger.info(
    "Collected %d articles",
    len(articles)
)

for article in articles:
    print(article)

