import time
import readCSV
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By



def getLinks(website):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Set to headless mode
    webdriver_service = Service('/usr/local/bin/chromedriver')

    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    driver.get(website)
    time.sleep(20)

    links = driver.find_elements(By.TAG_NAME, 'a')
 
    array = []
    for link in links:
        url = link.get_attribute('href')
        
        if url.startswith('https://www.producthunt.com/posts') and url not in array:
            array.append(url)

    driver.quit()
    return(array)



