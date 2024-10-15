import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

def fetch_hackathons(base_url, total_pages):
    all_hackathons = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }

    for page in range(1, total_pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            hackathons = data.get('hackathons', [])
            for hackathon in hackathons:
                title = hackathon.get('title')
                location = hackathon.get('location', 'Online')
                submission_period_dates = hackathon.get('submission_period_dates', 'N/A')
                hackathon_url = hackathon.get('url')

                all_hackathons.append({
                    'Source': 'Devpost',
                    'Title': title,
                    'Location': location,
                    'Dates': submission_period_dates,
                    'URL': hackathon_url
                })
        else:
            print(f"Failed to fetch data from Devpost page {page}, status code: {response.status_code}")  # Log error

    return all_hackathons

def scrape_mlh_hackathons():
    events = []
    url = "https://mlh.io/seasons/2025/events"
    
    # Set up a session and headers
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    
    # Fetch the MLH hackathons
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        # Extracting the necessary data from the HTML response
        soup = BeautifulSoup(html_content, 'html.parser')
        event_elements = soup.find_all('div', class_='event-wrapper')

        for event in event_elements:
            try:
                name = event.find('h3').get_text() if event.find('h3') else None
                event_url = event.find('a')['href'] if event.find('a') else None
                start_date = event.find('meta', itemprop='startDate')['content'] if event.find('meta', itemprop='startDate') else None
                end_date = event.find('meta', itemprop='endDate')['content'] if event.find('meta', itemprop='endDate') else None
                location = event.find('span', itemprop='city').get_text() if event.find('span', itemprop='city') else 'Digital Only'

                event_info = {
                    "Source": 'MLH',
                    "Title": name,
                    "Location": location,
                    "Dates": f"{start_date} - {end_date}",
                    "URL": event_url
                }
                events.append(event_info)
            except Exception as e:
                print(f"Error extracting data from MLH event: {e}")  # Log error
    else:
        print(f"Failed to fetch MLH events, status code: {response.status_code}")  # Log error

    return events

def main():
    st.title("Hackathon Dashboard")

    # Use a spinner while fetching hackathons
    with st.spinner("Fetching latest hackathons..."):
        # Devpost scraping
        base_url = "https://devpost.com/api/hackathons"
        total_pages = 100  # Adjust based on the number of pages you want to fetch
        devpost_hackathons = fetch_hackathons(base_url, total_pages)

        # MLH scraping
        mlh_events = scrape_mlh_hackathons()

    # Combine both datasets
    combined_hackathons = devpost_hackathons + mlh_events
    df_combined = pd.DataFrame(combined_hackathons)

    if not df_combined.empty:
        st.write(df_combined)
        csv_combined = df_combined.to_csv(index=False).encode('utf-8')
        st.download_button("Download Combined Hackathons CSV", csv_combined, "combined_hackathons.csv", "text/csv")
    else:
        st.warning("No hackathons found.")

if __name__ == "__main__":
    main()
