from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
import requests
from io import StringIO

# Setup Logging
logging.basicConfig(filename='crypto_scraping_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup Selenium WebDriver
def setup_driver():
    chrome_options = Options()
    # Comment out or remove the headless option to see the browser
    chrome_options.add_argument("--headless")  
    service = Service('D:/cllg/web scraping/web_scraping_project/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Define Data Scraping Function
def scrape_data(driver, url):
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Example for extracting tables using BeautifulSoup
    tables = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for i in range(1, 2):
        logging.info(f'Processing page {i}')
        params = {'page': i}
        
        response = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for table in soup.find_all('table'):
            try:
                html_str = str(table)
                df = pd.read_html(StringIO(html_str))[0]
                tables.append(df)
            except ValueError as e:
                logging.warning(f"Skipping table due to error: {e}")

    # Combine all DataFrames into one
    master_table = pd.concat(tables, ignore_index=True)

    # Clean up the DataFrame if needed (optional)
    master_table = master_table.loc[:, master_table.columns[1:-1]]

    return master_table

# Handle Pagination and Save Data
def scrape_with_pagination(driver, base_url, total_pages):
    all_data = []
    for page in range(1, total_pages + 1):
        url = f"{base_url}?page={page}"
        logging.info(f"Scraping page {page} at {url}")
        data = scrape_data(driver, url)
        if not data.empty:
            all_data.append(data)
        else:
            logging.info(f"No data found on page {page}")

    if all_data:
        master_table = pd.concat(all_data, ignore_index=True)
        save_to_excel(master_table)
        logging.info("Data scraping with pagination completed.")

# Save Data to Excel
def save_to_excel(data, filename='crypto_data.xlsx'):
    data.to_excel(filename, index=False)
    logging.info(f"Data saved to {filename}")

# Combine Everything
def scrape_with_logging(base_url, total_pages):
    driver = setup_driver()
    try:
        scrape_with_pagination(driver, base_url, total_pages)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        driver.quit()
        logging.info("WebDriver closed.")

if __name__ == "__main__":
    base_url = 'https://www.coingecko.com/en'
    total_pages = 1  # Adjust based on the number of pages you want to scrape
    scrape_with_logging(base_url, total_pages)
