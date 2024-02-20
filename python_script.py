from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import csv
import time

# Initialize a WebDriver
def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome('drivers\chromedriver.exe')
    return driver

# Function to search Google and return the search results
def google_search(query, driver):
    driver.get('https://www.google.com')
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Let the page load
    search_results = driver.find_elements(By.CSS_SELECTOR, 'div#search a')
    links = [result.get_attribute('href') for result in search_results if 'google' not in result.get_attribute('href')]
    return links[:5]

# Simplified scraping function; for demonstration purposes only
def scrape_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = ' '.join(soup.stripped_strings)
        return {'url': url, 'content': text_content[:500]}
    else:
        return {'url': url, 'content': 'Failed to retrieve content'}

# Function to generate PDF report
def generate_pdf_report(data):
    doc = SimpleDocTemplate("canoo_report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    for query, url, scraped_content in data:
        content.append(Paragraph(f"Query: {query}", styles['Title']))
        content.append(Paragraph(f"URL: {url}", styles['Normal']))
        content.append(Paragraph(f"Content: {scraped_content}", styles['Normal']))
        content.append(Paragraph("\n", styles['Normal']))

    doc.build(content)

# Main function
def main():
    driver = init_driver()

    queries = [
        "What is the outlook for the Canoo market in terms of size, growth, and trends from 2024 to 2030?",
        "What insights can be gathered about the Canoo market, including its size, share, trends, and forecasted growth for the years 2023 to 2030?",
        "What information is available about Canoo's presence on Wikipedia, and what does it reveal about the company?",
        "What is the market share, latest trends, and industry share for canoeing and kayaking equipment up to 2030?",
        "What insights can be gained from reports on the technology market size and future growth analysis up to 2031?",
        "How does Canoo's market share in 2024 compare, and what are the revenue and price trends, size, growth strategies, opportunities, and challenges forecasted until 2032?",
        "What details are provided about Canoo Inc.'s competitors in 2024, including stocks like GOEV on Macroaxis?",
        "How is Canoo's financial performance analyzed through income statements and other financial data?",
        "What are the stock forecasts, price targets, and analyst predictions for Canoo Inc. (GOEV) according to TipRanks.com?",
        "What are the stock forecasts, price targets, and analyst predictions for Canoo Inc. (GOEV) according to TipRanks.com?",
        "What insights can be derived from Canoo Inc.'s stock forecast and price targets, as analyzed in stock analysis reports?"
    ]

    scraped_data = []

    with open('canoo_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Query', 'URL', 'Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for query in queries:
            print(f"Searching for: {query}")
            search_results = google_search(query, driver)
            for url in search_results:
                data = scrape_data(url)
                writer.writerow({'Query': query, 'URL': data['url'], 'Content': data['content']})
                scraped_data.append((query, data['url'], data['content']))

    driver.quit()
    print("Data scraping and writing to CSV completed.")

    # Generate PDF report
    generate_pdf_report(scraped_data)

if __name__ == "__main__":
    main()