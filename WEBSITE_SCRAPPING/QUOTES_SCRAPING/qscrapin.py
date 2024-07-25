from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time

# Setup Logging
logging.basicConfig(filename='quotes_scraping_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup Selenium WebDriver
def setup_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Uncomment this line to run Chrome in headless mode
    chrome_options.add_argument("--start-maximized")
    service = Service('D:/cllg/web scraping/web_scraping_project/chromedriver-win64/chromedriver.exe')  # Update with the path to your WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Define Data Scraping Function
def scrape_data(driver, url):
    driver.get(url)
    time.sleep(3)  # Allow time for the page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = []

    for quote in soup.select('.quote'):
        text = quote.select_one('.text').get_text(strip=True)
        author = quote.select_one('.author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.select('.tag')]
        data.append({'Text': text, 'Author': author, 'Tags': ', '.join(tags)})

    return data

# Handle Pagination
def handle_pagination(driver, base_url):
    all_data = []
    page_number = 1

    while True:
        url = f"{base_url}/page/{page_number}/"
        logging.info(f"Scraping page {page_number} at {url}")
        data = scrape_data(driver, url)
        if not data:
            break  # Exit loop if no data is returned (last page reached)
        all_data.extend(data)
        page_number += 1

    return all_data

# Save Data to Excel
def save_to_excel(data, filename='quotes_data.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    logging.info(f"Data saved to {filename}")

# Combine Everything
def scrape_with_logging(base_url):
    driver = setup_driver()
    try:
        data = handle_pagination(driver, base_url)
        save_to_excel(data)
        logging.info(f"Data scraped successfully from {base_url}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    base_url = 'http://quotes.toscrape.com'
    scrape_with_logging(base_url)
