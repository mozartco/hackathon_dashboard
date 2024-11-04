# Hackathon Dashboard

![UI Screenshot](assets/UI.png)

### Demo
[Presentation Link](https://drive.google.com/file/d/1I4Ul9wisIMe4XE--m_v_gNxIlm1SU8pA/view?usp=sharing)

## Overview

The Hackathon Dashboard is a web application designed to scrape hackathon information from various sources such as Devpost, Devfolio, and MLH, consolidating the data into a single, user-friendly interface. This project aims to make it easier for developers and enthusiasts to find and participate in upcoming hackathons.

## Technologies Used

- **Web Scraping**: The application utilizes Python along with various scraping tools and packages to gather data from different platforms.
- **User Interface**: Built using [Streamlit](https://streamlit.io/), allowing for an interactive and responsive UI.
- **Scheduler**: CRON scheduler has been implemented via GitHub Actions to automate data scraping and updating processes.

## Getting Started

To run the Hackathon Dashboard locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/mozartco/hackathon_dashboard.git

2. Change directory:
    ```bash
    cd src

3. Run streamlit app:
    ```bash
    streamlit run hackathon_etl_pipeline.py
