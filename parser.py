from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

URL = ""

driver.get(URL)

driver.implicitly_wait(10)

# contents = driver.find_element(By.ID, "contents")

img_elements = driver.find_elements(By.TAG_NAME, "h1")

img_links = []

for img in img_elements:
    img_link = img #.get_attribute("src")
    if img_link:
        img_links.append(img_link)

print(img_links)
