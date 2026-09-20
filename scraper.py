import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.aps.dz"
SOURCE_URL = f"{BASE_URL}/en"

# =========================================
# Parse on article
# =========================================

def parse_article(article_url):
    article_response = requests.get(article_url)

    # Parse homepage HTML
    article_soup = BeautifulSoup(
        article_response.text,
        "html.parser"
    )

    title = article_soup.find("h1")

    date = article_soup.find("span", class_="text-xs")

    lead = article_soup.find("p")

    description = lead.get_text(" ", strip=True) if lead else None

    article = {
        "title": title.get_text(strip=True) if title else None,
        "url": article_url,
        "date": date.get_text(strip=True) if date else None,
        "description": description
    }

    return article


# =========================================
# Fetch homepage
# =========================================

response = requests.get(SOURCE_URL)
print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

# =========================================
# Find article URLs
# =========================================

article_urls = set()

for link in soup.find_all("a"):
    image = link.find("img")

    if image:
        src = image.get("src")

        if "image%2Farticle" in src:
            article_urls.add(link.get("href"))

print("Found", len(article_urls), "unique articles")


# =========================================
# Parse articles
# =========================================

articles = []

for article_path in article_urls:

    article_url = BASE_URL + article_path

    article = parse_article(article_url)

    articles.append(article)

print("Collected:", len(articles), "articles")

for article in articles:
    print(article)
   