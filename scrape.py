import requests
from bs4 import BeautifulSoup

# =====================================
# 1. Request APS homepage
# =====================================

url = "https://www.aps.dz/en"

response = requests.get(url)

print(response.status_code)
print("Length:", len(response.text))

# Experimment: searching raw HTML for the word "article"
# print("article:", response.text.lower().count("article"))

# html = response.text.lower()
# position = html.find("article")
# print(html[position - 200:position + 500])

# =====================================
# 2.Parse HTML with BeautifulSoup
# =====================================

soup = BeautifulSoup(response.text, "html.parser")

# First <a> element on the page
link = soup.find("a")
print(link.get("href"))
print(link.get_text(strip=True))

# Number of <a> elements on the page
links = soup.find_all("a")
print(len(links))

# Find a specific article
article_link = soup.find(
    "a",
    href=lambda href: href and "mu4dbg9h" in href
)

print(article_link.get("href"))

# Extract title
title = article_link.find("h2")
print(title.get_text(strip=True))

# Extract date
date = article_link.find("p")
print(date.get_text(strip=True))

# Build the full article URL
article_url = "https://www.aps.dz" + article_link.get("href")
print(article_url)

# Request the individual article page
article_response = requests.get(article_url)

print(article_response.status_code)
print(len(article_response.text))

article_soup = BeautifulSoup(article_response.text, "html.parser")

# Experiment: searching for the exact h element for the title
# print(article_soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]))

# Extract the title
title = article_soup.find("h1")
print(title.get_text(strip=True))

# Experiment:
# print(article_soup.get_text(strip=True)[:3000])

lead = article_soup.find(
    string=lambda text: text and "ALGIERS - The President of the Republic" in text
)

# print(lead)
# print(lead.parent)

description = lead.parent.get_text(strip=True)
print(description)

"""

for link in links:
    href = link.get("href")

    if href and "news" in href:
        print(href)

for link in links:
    title = link.find(["h2", "h3"])

    if title:
        print(title.get_text(strip=True))

article_link = soup.find(
    "a",
    href=lambda href: href and "mu5nkqag" in href
)

print(article_link)


print(article_link.get("class"))

title = article_link.find(["h2", "h3"])
print(title.get("class"))

dossier_link = soup.find(
    "a",
    href=lambda href: href and "mn35o7nd" in href
)

print(dossier_link)


article_image = article_link.find("img")
print(article_image.get("src"))

dossier_image = dossier_link.find("img")
print(dossier_image.get("src"))
"""

article_urls = set()

for link in links:
    image = link.find("img")

    if image:
        src = image.get("src")

        if "image%2Farticle" in src:
            article_urls.add(link.get("href"))

print(article_urls)
print("Number of unique articles:", len(article_urls))