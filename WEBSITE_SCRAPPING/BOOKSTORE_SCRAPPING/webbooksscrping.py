from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time

# Setup Logging
logging.basicConfig(filename='scraping_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup Selenium WebDriver
def setup_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Run in headless mode for automation
    chrome_options.add_argument("--start-maximized") 
    service = Service('D:\cllg\web scraping\web_scraping_project\chromedriver-win64\chromedriver.exe')  # Update with the path to your WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Define Data Scraping Function
def scrape_data(driver, url):
    driver.get(url)
    time.sleep(3)  # Allow time for the page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = []

    for item in soup.select('article.product_pod'):
        name = item.select_one('h3 > a').attrs['title']
        price = item.select_one('.price_color').text.strip()
        data.append({'Name': name, 'Price': price})
    
    return data

# Handle Pagination
def handle_pagination(driver, base_url, total_pages):
    all_data = []
    for page in range(1, total_pages + 1):
        url = f"{base_url}/catalogue/page-{page}.html"
        logging.info(f"Scraping page {page} at {url}")
        data = scrape_data(driver, url)
        all_data.extend(data)
    return all_data

# Save Data to Excel
def save_to_excel(data, filename='scraped_data.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    logging.info(f"Data saved to {filename}")

# Combine Everything
def scrape_with_logging(base_url, total_pages):
    driver = setup_driver()
    try:
        data = handle_pagination(driver, base_url, total_pages)
        save_to_excel(data)
        logging.info(f"Data scraped successfully from {base_url}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    base_url = '    '
    total_pages = 5  # Adjust based on the number of pages you want to scrape
    scrape_with_logging(base_url, total_pages)
