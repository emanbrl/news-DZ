import requests
from bs4 import BeautifulSoup

url = "https://www.aps.dz/en"

response = requests.get(url)

print(response.status_code)
print("Length:", len(response.text))
print("article:", response.text.lower().count("article"))

html = response.text.lower()
position = html.find("article")
# print(html[position - 200:position + 500])

#--------------#

soup = BeautifulSoup(response.text, "html.parser")
link = soup.find("a")
print(link.get("href"))
print(link.get_text(strip=True))

links = soup.find_all("a")
print(len(links))

article_link = soup.find("a", href=lambda href: href and "mu4dbg9h" in href)
print(article_link.get("href"))

title = article_link.find("h2")
print(title.get_text(strip=True))

date = article_link.find("p")
print(date.get_text(strip=True))

article_url = "https://www.aps.dz" + article_link.get("href")
print(article_url)

article_response = requests.get(article_url)

print(article_response.status_code)
print(len(article_response.text))