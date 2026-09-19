import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.aps.dz"
SOURCE_URL = f"{BASE_URL}/en"

# =========================================
# Fetch homepage
# =========================================

response = requests.get(SOURCE_URL)
print(response.status_code)

# Parse homepage HTML
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

articles = []

for article_path in article_urls:

    article_url = BASE_URL + article_path

    article_response = requests.get(article_url)

    article_soup = BeautifulSoup(
        article_response.text,
        "html.parser"
    )

    title = article_soup.find("h1")

    date = article_soup.find("span", class_="text-xs")

    lead = article_soup.find(
        string=lambda text: text and text.startswith("ALGIERS -")
    )

    description = lead.parent.get_text(strip=True) if lead else None

    article = {
        "title": title.get_text(strip=True) if title else None,
        "url": article_url,
        "date": date.get_text(strip=True) if date else None,
        "description": description,
    }

    articles.append(article)

print("Collected:", len(articles), "articles")

for article in articles:
    print(article)
   