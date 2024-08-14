# Python Projects

Welcome to my collection of Python projects! This repository showcases three different applications developed using Python and the Flask framework. Each project demonstrates various aspects of web development and data handling.

## Projects

### 1. Website Scraping

**Description:**  
This project involves scraping data from a website to extract relevant information using Python. The scraping script utilizes libraries such as BeautifulSoup and Selenium to handle dynamic content and pagination. The extracted data is processed and saved for further analysis.

**Features:**
- Web scraping of live data
- Handling JavaScript content with Selenium
- Data cleaning and processing
- Saving data to an Excel file

**How to Run:**
1. Install required libraries: `pip install beautifulsoup4 selenium pandas openpyxl`
2. Download the appropriate WebDriver for Selenium.
3. Run the script: `python scrape.py`

**Files:**
- `scrape.py` - Main script for scraping data
- `requirements.txt` - List of dependencies

### 2. Weather App

**Description:**  
This application provides real-time weather information for any city using the OpenWeatherMap API. Built with Python and Flask, the app fetches weather data, processes it, and displays it in a user-friendly format.

**Features:**
- Real-time weather data
- Search functionality for different cities
- Display of temperature, weather conditions, and other details

**How to Run:**
1. Install required libraries: `pip install flask requests`
2. Set up your OpenWeatherMap API key in the `config.py` file.
3. Run the Flask application: `python app.py`
4. Access the app at `http://127.0.0.1:5000`

**Files:**
- `app.py` - Main Flask application
- `config.py` - Configuration file with API key
- `templates/` - HTML templates for the app
- `static/` - CSS and JavaScript files

### 3. To-Do List App

**Description:**  
A simple to-do list application built using Python and Flask. This app allows users to add, edit, and delete tasks, and stores the data locally.

**Features:**
- Add, edit, and delete tasks
- Persistent storage of tasks
- User-friendly interface

**How to Run:**
1. Install required libraries: `pip install flask`
2. Run the Flask application: `python app.py`
3. Access the app at `http://127.0.0.1:5000`

**Files:**
- `app.py` - Main Flask application
- `templates/` - HTML templates for the app
- `static/` - CSS files for styling

## Installation

Clone the repository:
```bash
git clone https://github.com/Vehement2003/Python_projects.git
