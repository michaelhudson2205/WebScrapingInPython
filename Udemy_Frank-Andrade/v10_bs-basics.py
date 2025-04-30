#
# ! pip install bs4
# ! pip install requests
# ! pip install lxml

from bs4 import BeautifulSoup
import requests

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
