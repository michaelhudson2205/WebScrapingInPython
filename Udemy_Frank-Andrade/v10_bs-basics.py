#
# ! pip install bs4
# ! pip install requests
# ! pip install lxml

from bs4 import BeautifulSoup
import requests
import time

website = "https://subslikescript.com/movie/Titanic-120338"
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, "lxml")
print(soup.prettify())

box = soup.find("article", class_="main-article")

title = box.find("h1").get_text()

transcript = box.find("div", class_="full-script").get_text(strip=True, separator=" ")

# print(title)
# print(transcript)

with open(f"{title}.txt", "w") as my_file:
    my_file.write(title)
    my_file.write("\n")
    my_file.write(transcript)
    my_file.write("\n")

# * =====================================================
# Video 15 - Scraping multiple links within the same page

root = "https://subslikescript.com"
website_m = f"{root}/movies"
result_m = requests.get(website_m)
content_m = result_m.text
soup_m = BeautifulSoup(content_m, "lxml")

box_m = soup_m.find("article", class_="main-article")

links = []
for link in box_m.find_all("a", href=True):
    links.append(link["href"])

print(links)
len(links)

for link in links:
    time.sleep(2)
    website = f"{root}{link}"
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content, "lxml")
    box = soup.find("article", class_="main-article")
    title = box.find("h1").get_text()
    transcript = box.find("div", class_="full-script").get_text(
        strip=True, separator=" "
    )
    with open(f"{title}.txt", "w", encoding="utf-8") as my_file:
        my_file.write(title)
        my_file.write("\n")
        my_file.write(transcript)
        my_file.write("\n")
