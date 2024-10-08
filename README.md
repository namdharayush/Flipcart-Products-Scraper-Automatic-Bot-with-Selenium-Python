![Banner Image](flipkart.png)

# Flipkart Products Scraper - Automatic Bot with Selenium and Python

## Overview

Welcome to the **Flipkart Products Scraper** repository! This Python-based web scraper automates the extraction of product data from Flipkart. Utilizing Selenium for dynamic web interactions, it captures detailed product information and stores it in MongoDB. The scraper also supports exporting data to CSV, Excel, and JSON formats for comprehensive analysis.

## Key Features

- **Automated Scraping:** Seamlessly navigates Flipkart pages to search and extract product data based on user-defined keywords.
- **Comprehensive Data Extraction:** Retrieves essential product details such as title, images, specifications, price, and more.
- **MongoDB Integration:** Efficiently stores scraped data in MongoDB with unique indexing to prevent duplicates.
- **Flexible Data Export:** Exports data into CSV, Excel, and JSON formats for versatile use.
- **Robust Error Handling:** Incorporates retry mechanisms to manage network or data retrieval issues effectively.

## Components

- **`flipkart.py`:** Initiates the Selenium WebDriver, performs product searches on Flipkart, and saves product URLs to MongoDB.
- **`flipkart_scrap.py`:** Processes product URLs from MongoDB, extracts detailed information, and updates the database.
- **`flipkartMongo.py`:** Handles MongoDB connections, data insertion, and ensures unique indexing on product links.

## Prerequisites

- **Python 3.7+**: Ensure Python is installed on your system.
- **MongoDB**: Must be installed and running. Configure `flipkartMongo.py` if using a remote instance.
- **Google Chrome**: Ensure you have the latest version of Chrome installed.
- **Chromedriver**: Download and place the Chromedriver executable in your system's PATH.
- **Python Libraries**: Install required libraries with:

    ```bash
    pip install -r requirements.txt
    ```

## Installation Guide

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/namdharayush/Flipkart-Products-Scraper-Automatic-Bot-with-Selenium-Python.git
    cd Flipkart-Products-Scraper-Automatic-Bot-with-Selenium-Python
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure MongoDB:**
    - Make sure MongoDB is running locally or update the connection string in `flipkartMongo.py` for a remote MongoDB instance.

4. **Setup Chromedriver:**
    - Download the appropriate Chromedriver for your Chrome version from [Chromedriver Downloads](https://googlechromelabs.github.io/chrome-for-testing/).
    - Add the Chromedriver executable to your system's PATH.

## How to Use

1. **Run the Selenium Scraper:**

    ```bash
    python flipkart.py
    ```

    This script starts a browser session, searches for products on Flipkart, and saves product URLs to MongoDB.

2. **Scrape Product Details:**

    ```bash
    python flipkart_scrap.py
    ```

    This script processes the saved URLs, extracts detailed product information, and updates the MongoDB collection.

3. **Export Data:**
    - Export scraped data to CSV, Excel, or JSON formats using the methods defined in `flipkart_scrap.py`.

## Customization

- **Modify Search Keywords:** Adjust the keywords in `flipkart.py` to target different product categories.
- **Update MongoDB Connection:** Change the connection string in `flipkartMongo.py` if using a different MongoDB server.
- **Adjust Data Fields:** Modify the data extraction logic in `flipkart_scrap.py` as needed.


## Contact

For questions or support, open an issue on [GitHub](https://github.com/namdharayush/Flipkart-Products-Scraper-Automatic-Bot-with-Selenium-Python/issues).

## Acknowledgements

Thanks for checking out the Flipkart Products Scraper! Feel free to explore and contribute to make it better.
