import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fetch hackathons from Devpost
def fetch_devpost_hackathons(base_url, total_pages):
    all_hackathons = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for page in range(1, total_pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            hackathons = data.get('hackathons', [])
            for hackathon in hackathons:
                all_hackathons.append({
                    'Title': hackathon.get('title'),
                    'Location': hackathon.get('location', 'Online'),
                    'Dates': hackathon.get('submission_period_dates', 'N/A'),
                    'URL': hackathon.get('url')
                })
        else:
            logging.error(f"Failed to fetch Devpost page {page}. Status code: {response.status_code}")
            break

    return all_hackathons

# Fetch hackathons from MLH
def fetch_mlh_hackathons(base_url):
    all_hackathons = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        events = soup.find_all('div', class_='event')

        for event in events:
            title = event.find('h3', class_='event-name').get_text(strip=True) if event.find('h3', class_='event-name') else 'N/A'
            dates = event.find('p', class_='event-date').get_text(strip=True) if event.find('p', class_='event-date') else 'N/A'
            location = event.find('div', class_='event-location').get_text(strip=True) if event.find('div', class_='event-location') else 'Online'
            url = event.find('a', class_='event-link')['href'] if event.find('a', class_='event-link') else 'N/A'

            all_hackathons.append({
                'Title': title,
                'Location': location,
                'Dates': dates,
                'URL': url
            })
    else:
        logging.error(f"Failed to fetch MLH data. Status code: {response.status_code}")

    return all_hackathons

# Save data to CSV
def save_to_csv(data, file_path):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        logging.info(f"Data saved to {file_path}")
    else:
        logging.warning("No data to save.")

# Combine and clean data
def combine_and_clean_csv(devpost_path, mlh_path, combined_path):
    df_devpost = pd.read_csv(devpost_path)
    df_mlh = pd.read_csv(mlh_path)
    df_combined = pd.concat([df_devpost, df_mlh]).drop_duplicates().reset_index(drop=True)
    df_combined.to_csv(combined_path, index=False)
    logging.info(f"Combined data saved to {combined_path}")

# Main ETL function
def run_etl():
    base_url_devpost = "https://devpost.com/api/hackathons"
    base_url_mlh = "https://mlh.io/seasons/2025/events"
    devpost_data = fetch_devpost_hackathons(base_url_devpost, 5)
    mlh_data = fetch_mlh_hackathons(base_url_mlh)

    # File paths within the repository
    devpost_csv = "data/devpost.csv"
    mlh_csv = "data/mlh.csv"
    combined_csv = "data/combined_hackathons.csv"

    # Save CSVs locally
    save_to_csv(devpost_data, devpost_csv)
    save_to_csv(mlh_data, mlh_csv)

    # Combine and clean
    combine_and_clean_csv(devpost_csv, mlh_csv, combined_csv)

if __name__ == "__main__":
    run_etl()
