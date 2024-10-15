# Source Code

This directory contains the source code for the Hackathon Dashboard project, including scripts for data scraping and the frontend interface.

## Directory Structure

- **scrapers/**: Contains scripts used to scrape hackathon data from Devpost and MLH.
  - `devpost_scraper.py`: This script fetches hackathon data from the Devpost API using the `requests` library. It handles pagination and extracts relevant information, such as title, location, submission period dates, and URL.
  - `mlh.py`: Script to scrape hackathon data from MLH using API calls. 
  

- **frontend/**: Contains code for the frontend, which is built using Streamlit.
  - `scrape.py.py`: The main Streamlit application file that powers the dashboard. It allows users to filter hackathons by location, number of registrations, submission deadlines, and online/offline modes.

