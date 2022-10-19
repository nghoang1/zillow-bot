from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
DOC_URL = "https://docs.google.com/forms/d/e/1FAIpQLScrWc2F7fFnS1WYGxdIUQlg97jn2p5CjWXHLmGSAA3BNeNQgw/viewform?usp=sf_link"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
}

response = requests.get(ZILLOW_URL, headers=headers)
zillow_website = response.text
prices_list = []
#links_list = []
addresses_list = []
soup = BeautifulSoup(zillow_website,"html.parser")
for el in (soup.find_all(class_="list-card-price")):
    prices_list.append(el.getText())

for el in (soup.find_all(class_="list-card-addr")):
    addresses_list.append(el.getText())

href= (soup.find_all("a", class_="list-card-link"))

links_list = [a["href"] for a in soup.find_all(name = "a", class_ = 'list-card-link', tabindex="0")]
print(len(prices_list))
print(len(addresses_list))
print(len(links_list))
chrome_driver_path = r"C:\Users\hoang\Desktop\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(DOC_URL)
time.sleep(3)
for i in range(len(addresses_list)):
    input_adress = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_adress.send_keys(addresses_list[i])

    input_price = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_price.send_keys(prices_list[i])

    input_link =  driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_link.send_keys(links_list[i])

    submit_btn = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_btn.click()
    time.sleep(3)
    another_one = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    another_one.click()
time.sleep(300)
driver.quit()

