
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['smartmaple']
collection = db['kitapyurdu']
options = Options()
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get('https://www.kitapyurdu.com/')
time.sleep(2)
try:
    allBestSellers = driver.find_element(By.XPATH, '//*[@id="js-bestseller"]/div[2]/div[2]/a')
    allBestSellers.click()
    time.sleep(2)
except Exception as e:
    print("Error:", e)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
categoryList = soup.find_all("a", {"style": "margin-bottom: 2px;"})
for category in categoryList:
    driver.get(category.get("href"))
    time.sleep(1)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    lastPage = driver.find_element(By.CSS_SELECTOR, 'a.last')
    href_attribute = lastPage.get_attribute('href')
    parsed_url = urlparse(href_attribute)
    query_params = parse_qs(parsed_url.query)
    totalPage = int(query_params.get('page', [None])[0])


    titleLinks = soup.find_all("div", {"class": "name ellipsis"})
    prices = soup.find_all("div", {"class": "price-new"})
    authors = soup.find_all("div", {"class": "author compact ellipsis"})
    publishers = soup.find_all("div", {"class": "publisher"})
    for titleLink, price, author, publisher in zip(titleLinks, prices, authors, publishers):
        data = {}
        bookTitle = titleLink.find("span").text.strip() if titleLink.find("span") else None
        bookLink = titleLink.find("a").get("href")
        bookPrice = price.find("span", {"class": "value"}).text.strip() if price.find("span",
                                                                                      {"class": "value"}) else None
        bookAuthor = author.find("a", {"class": "alt"}).text.strip() if author.find("a", {"class": "alt"}) else None
        bookPublisher = publisher.find("a", {"class": "alt"}).text.strip() if publisher.find("a",
                                                                                             {"class": "alt"}) else None
        data.update({
            'title': bookTitle,
            'price': bookPrice,
            'publisher': bookPublisher,
            'writers': bookAuthor,
            'link': bookLink
        })
        inserted_data = collection.insert_one(data)
        time.sleep(1)
        print("Inserted Document ID:", inserted_data.inserted_id)
    time.sleep(2)
    pageCount = 1
    while pageCount < totalPage:
        try:
            allBestSellersNext = driver.find_element(By.CSS_SELECTOR, 'a.next')
            allBestSellersNext.click()
            time.sleep(2)
            page_source = driver.page_source
            soupOther = BeautifulSoup(page_source, 'html.parser')

            titleLinks = soupOther.find_all("div", {"class": "name ellipsis"})
            prices = soupOther.find_all("div", {"class": "price-new"})
            authors = soupOther.find_all("div", {"class": "author compact ellipsis"})
            publishers = soupOther.find_all("div", {"class": "publisher"})
            for titleLink, price, author, publisher in zip(titleLinks, prices, authors, publishers):
                data = {}
                time.sleep(1)
                bookTitle = titleLink.find("span").text.strip() if titleLink.find("span") else None
                bookLink = titleLink.find("a").get("href")
                bookPrice = price.find("span", {"class": "value"}).text.strip() if price.find("span", {
                    "class": "value"}) else None
                bookAuthor = author.find("a", {"class": "alt"}).text.strip() if author.find("a",
                                                                                            {"class": "alt"}) else None
                bookPublisher = publisher.find("a", {"class": "alt"}).text.strip() if publisher.find("a", {
                    "class": "alt"}) else None
                data.update({
                    'title': bookTitle,
                    'price': bookPrice,
                    'publisher': bookPublisher,
                    'writers': bookAuthor,
                    'link': bookLink
                })
                inserted_data = collection.insert_one(data)
                time.sleep(1)
                print("Inserted Document ID:", inserted_data.inserted_id)
            time.sleep(2)
            pageCount += 1
        except Exception as ex:
            print("exceptionda", ex)
            pass

time.sleep(5)
driver.close()
client.close()
