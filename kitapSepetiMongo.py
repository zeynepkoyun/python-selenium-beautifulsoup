
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pymongo
from selenium.common.exceptions import NoSuchElementException

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['smartmaple']
collection = db['kitapsepeti']
options = Options()
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get('https://www.kitapsepeti.com/')
time.sleep(2)


try:
    allBestSeller = driver.find_element(By.CSS_SELECTOR, "#mainColumn > div.col.col-12 > div > a > img")
    allBestSeller.click()
    time.sleep(1)
except Exception as ex:
    print("Error:", ex)

allBestSellerSale = driver.find_element(By.XPATH,"//*[@id='filtreStock']/div/div/div/div/label")
allBestSellerSale.click()
time.sleep(1)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

titleLinkPublisherAuthors = soup.find_all("div", {"class":"box col-12 text-center"})
prices = soup.find_all("div", {"class":"col col-12 currentPrice"})
for titleLinkPublisherAuthor,price in zip(titleLinkPublisherAuthors,prices):
    data = {}
    bookTitle = titleLinkPublisherAuthor.find("a",{"class":"fl col-12 text-description detailLink"}).get("title")
    bookLink = titleLinkPublisherAuthor.find("a",{"class":"fl col-12 text-description detailLink"}).get("href")
    bookPublisher = titleLinkPublisherAuthor.find("a",{"class":"col col-12 text-title mt"}).text.strip()
    bookAuthor = titleLinkPublisherAuthor.find("a",{"class":"fl col-12 text-title"}).text.strip()
    bookPrice = price.text.strip().replace("\n","")
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

while driver.find_element(By.CSS_SELECTOR,'a.next'):
    allBestSellersNext = driver.find_element(By.CSS_SELECTOR, 'a.next')
    allBestSellersNext.click()
    time.sleep(1)
    try:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        titleLinkPublisherAuthors = soup.find_all("div", {"class": "box col-12 text-center"})
        prices = soup.find_all("div", {"class": "col col-12 currentPrice"})
        for titleLinkPublisherAuthor, price in zip(titleLinkPublisherAuthors, prices):
            data={}
            bookTitle = titleLinkPublisherAuthor.find("a", {"class": "fl col-12 text-description detailLink"}).get(
                "title")
            bookLink = titleLinkPublisherAuthor.find("a", {"class": "fl col-12 text-description detailLink"}).get(
                "href")
            bookPublisher = titleLinkPublisherAuthor.find("a", {"class": "col col-12 text-title mt"}).text.strip()
            bookAuthor = titleLinkPublisherAuthor.find("a", {"class": "fl col-12 text-title"}).text.strip()
            bookPrice = price.text.strip().replace("\n", "")
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

        if driver.find_element(By.CSS_SELECTOR, 'a.next.passive'): #sayfasonu
            break
    except NoSuchElementException as ex:
        pass
time.sleep(2)
driver.close()
client.close()