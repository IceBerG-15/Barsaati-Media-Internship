from selenium import webdriver  # Importing Selenium for web automation
from selenium.webdriver.common.by import By  # For locating elements
from selenium.webdriver.chrome.service import Service  # For ChromeDriver service management
from selenium.webdriver.chrome.options import Options  # For Chrome options configuration
from selenium.webdriver.common.proxy import Proxy, ProxyType  # For setting up proxies
from selenium.webdriver.common.keys import Keys  # For sending keyboard keys to elements
from bs4 import BeautifulSoup  # For HTML parsing
import time  # For adding delays
import requests  # For making HTTP requests
from pymongo import MongoClient  # For MongoDB interaction
import datetime  # For working with date and time
from dotenv import load_dotenv
import os

# Replace with the correct path to ChromeDriver
driver_path = "N:\\chromedriver\\chromedriver.exe"

load_dotenv("baraathi internshalla\\.env")

# Replace with your ProxyMesh credentials
proxymesh_user = os.getenv('proxymesh_user')
proxymesh_pass = os.getenv('proxymesh_pass')

# Twitter credentials
X_EMAIL = os.getenv('X_EMAIL')
X_PASS = os.getenv('X_PASS')
X_USER = os.getenv('X_USER')

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client.twitter_trends
collection = db.trends

# ProxyMesh Configuration
def get_proxy():
    # Basic method to get a ProxyMesh IP; can be adjusted based on subscription details
    return f"http://{proxymesh_user}:{proxymesh_pass}@us-ca.proxymesh.com:31280"

# Selenium Configuration
def get_driver(proxy_ip):
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument("--start-maximized")  # Starting Chrome maximized
    
    if proxy_ip:
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = proxy_ip
        prox.ssl_proxy = proxy_ip
        
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        capabilities['proxy'] = prox.to_capabilities()
        driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=chrome_options)
    else:
        driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=chrome_options)
    
    return driver

def login_twitter(driver):
    # Function to login to Twitter
    driver.get('https://x.com/login')
    time.sleep(5)  # Allow time for page to load
    email = driver.find_element(By.CSS_SELECTOR, "[name='text']")  # Find email input field
    email.send_keys(X_USER)  # Enter email
    time.sleep(1)
    email.send_keys(Keys.ENTER)  # Press enter
    time.sleep(4)  # Allow time for page to load
    password = driver.find_element(By.CSS_SELECTOR, "[name='password']")  # Find password input field
    password.send_keys(X_PASS)  # Enter password
    time.sleep(1)
    password.send_keys(Keys.ENTER)  # Press enter
    time.sleep(4)  # Allow time for page to load

def get_trending_topics(driver):
    # Function to scrape trending topics from Twitter
    driver.get('https://x.com/home')
    time.sleep(6)  # Allow time for page to load
    hashtags = []  # List to store scrapped hashtags
    page_source = driver.page_source  # Get page source
    soup = BeautifulSoup(page_source, 'html.parser')  # Parse HTML

    # Find all elements with data-testid='trend'
    trend_divs = soup.find_all('div', {'data-testid': 'trend'})

    # Extract text inside the <span> tags within each trend_div
    for trend_div in trend_divs:
        span = trend_div.find_all('span')
        if span:
            hashtags.append(span[1].text)  # Append text to hashtags list
    
    return hashtags

def current_ip_address():
    # Function to get current IP address
    proxy_url = "http://us-ca.proxymesh.com:31280"
    # Make a request to a service that reflects back the requester's IP address
    response = requests.get('http://httpbin.org/ip', proxies={'http': proxy_url, 'https': proxy_url}, auth=(proxymesh_user, proxymesh_pass))
    # Extract the IP address from the response
    ip_address = response.json()['origin']
    return ip_address

def adding_data_into_database(hashtags):
    # Function to add scraped data into MongoDB
    trending = {
                'nameoftrend1': hashtags[0],
                'nameoftrend2': hashtags[1],
                'nameoftrend3': hashtags[2],
                'nameoftrend4': hashtags[3],
                'nameoftrend5': hashtags[4],
                'date': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                'ip_address': current_ip_address()
            }
    collection.insert_one(trending)

def main():
    proxy_ip = get_proxy()
    driver = get_driver(proxy_ip)
    try:
        login_twitter(driver)
        hashtags = get_trending_topics(driver)
        adding_data_into_database(hashtags)
    except Exception as exc:
        print('An exception occurred: ', exc)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
