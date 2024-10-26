import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import csv
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_devpost_hackathons(base_url, total_pages):
    all_hackathons = []
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    for page in range(1, total_pages + 1):
        url = f"{base_url}?page={page}"
        logging.info(f"Fetching data from URL: {url}")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            logging.info(f"Successfully fetched data from page {page}")
            data = response.json()
            hackathons = data.get('hackathons', [])
            for hackathon in hackathons:
                title = hackathon.get('title')
                location = hackathon.get('location', 'Online')
                submission_period_dates = hackathon.get('submission_period_dates', 'N/A')
                hackathon_url = hackathon.get('url')

                all_hackathons.append({
                    'Title': title,
                    'Location': location,
                    'Dates': submission_period_dates,
                    'URL': hackathon_url
                })
        else:
            logging.error(f"Failed to fetch data from page {page}. Status code: {response.status_code}")

    return all_hackathons

def fetch_mlh_hackathons(base_url):
    all_hackathons = []
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    logging.info(f"Fetching data from URL: {base_url}")
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        logging.info("Successfully fetched data")
        soup = BeautifulSoup(response.text, 'html.parser')
        hackathons = soup.find_all('div', class_='event')

        for hackathon in hackathons:
            title_tag = hackathon.find('h3', class_='event-name')
            title = title_tag.get_text(strip=True) if title_tag else 'N/A'
            date_tag = hackathon.find('p', class_='event-date')
            dates = date_tag.get_text(strip=True) if date_tag else 'N/A'
            location_tag = hackathon.find('div', class_='event-location')
            location = location_tag.get_text(strip=True) if location_tag else 'Online'
            url_tag = hackathon.find('a', class_='event-link')
            hackathon_url = url_tag['href'] if url_tag else 'N/A'

            all_hackathons.append({
                'Title': title,
                'Location': location,
                'Dates': dates,
                'URL': hackathon_url
            })
    else:
        logging.error(f"Failed to fetch data. Status code: {response.status_code}")

    return all_hackathons

def save_to_csv(data, file_name):
    if data:
        fieldnames = ['Title', 'Location', 'Dates', 'URL']
        file_path = os.path.join("data", file_name)  # Save to the data folder
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow(item)
        logging.info(f"Data saved to {file_path}")
    else:
        logging.warning(f"No data to save in {file_name}")

def combine_and_clean(devpost_file, mlh_file, combined_file):
    devpost_path = os.path.join("data", devpost_file)
    mlh_path = os.path.join("data", mlh_file)
    combined_path = os.path.join("data", combined_file)

    # Check if the Devpost and MLH files exist
    df_devpost = pd.read_csv(devpost_path) if os.path.exists(devpost_path) else pd.DataFrame()
    df_mlh = pd.read_csv(mlh_path) if os.path.exists(mlh_path) else pd.DataFrame()

    if df_devpost.empty and df_mlh.empty:
        logging.warning("No data available in both Devpost and MLH datasets to combine.")
        return

    # Combine and clean
    df_combined = pd.concat([df_devpost, df_mlh]).drop_duplicates().reset_index(drop=True)
    df_combined.to_csv(combined_path, index=False)
    logging.info(f"Combined and cleaned data saved to {combined_path}")

# Main execution function
def hackathon_etl_pipeline():
    # Devpost scraping
    devpost_url = "https://devpost.com/api/hackathons"
    total_pages = 5
    devpost_file = "devpost.csv"
    logging.info("Starting Devpost hackathon scraper.")
    devpost_data = fetch_devpost_hackathons(devpost_url, total_pages)
    save_to_csv(devpost_data, devpost_file)

    # MLH scraping
    mlh_url = "https://mlh.io/seasons/2025/events"
    mlh_file = "mlh.csv"
    logging.info("Starting MLH hackathon scraper.")
    mlh_data = fetch_mlh_hackathons(mlh_url)
    save_to_csv(mlh_data, mlh_file)

    # Combine and clean data
    combined_file = "combined_hackathons.csv"
    combine_and_clean(devpost_file, mlh_file, combined_file)

if __name__ == "__main__":
    hackathon_etl_pipeline()
