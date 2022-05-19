import asyncio
import aiohttp
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

async def get_html(i):
    url = f"https://auto.ru/cars/toyota/all/?page={i}"
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service("chromedriver/chromedriver.exe")

    try:
        driver =  webdriver.Chrome(service=service, options=options)
        driver.get(url=url)
        time.sleep(2)
        html = driver.page_source

    finally:
        driver = webdriver.Chrome(service=service, options=options)
        driver.close()
        driver.quit()

    return html

async def gather_data():

    html = await get_html(1)
    soup = BeautifulSoup(html, "html.parser")
    pagination = int(soup.find("span", class_="ListingPagination__pages").find_all("a", class_="Button")[-1].text)

    task_list = []

    for i in range(1, pagination+1):
        task = asyncio.create_task(get_data(i))
        task_list.append(task)

    await asyncio.gather(*task_list)

async def get_data(i):
    html = await get_html(i)
    soup = BeautifulSoup(html, "html.parser")
    cars = soup.find_all("div", class_="ListingItem")
    for item in cars:
        car_link = item.find("a", class_="ListingItemTitle__link").get("href")
        car_name = item.find("a", class_="Link ListingItemTitle__link").text
        # car_prise = item.find("div", class_="ListingItemPrice ListingItem__price").text
        print(car_name)
        # print(car_prise)
        print(car_link)
        print("----------------------------------------------------------------------")
    print(" ")
    print(f"[INFO] Обработал страницу {i}")
    print(" ")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(gather_data())