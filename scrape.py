# python3 -m pip install requests
# => get data from web(html, json, xml)
# python3 -m pip install beautifulsoup4
# => parse html


# First time
# install git 
# git config --global user.name "Ramesh Pradhan"
# git config --global user.email "pyrameshpradhan@gmail.com"
# create a repository in github
# copy paste git code from github


# Always
# git add .
# git commit -m "Your message"


import requests
from bs4 import BeautifulSoup
import json
import csv


url = "http://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        return
    
    # set encoding explicitly to handle special character 
    response.encoding = response.apparent_encoding


    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    all_books = []
    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text
        currency = price_text[0]
        price = float(price_text[1:])
        book = {
            "title": title,
            "currency": currency,
            "price": price,
        }
        all_books.append(book)

    return all_books


all_books = scrape_books(url)

# json
with open('books.json', 'w', encoding='utf-8') as f:

    json.dump(all_books, f, indent=2, ensure_ascii=False)

# csv
with open("books.csv", "w", newline="", encoding="utf-8") as f:
    
    writer = csv.DictWriter(f, fieldnames=["title", "currency", "price"])
    writer.writeheader()
    writer.writerows(all_books)