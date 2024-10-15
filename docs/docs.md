# Methodology

## Data Collection
Hackathon data is collected from Devpost and Devfolio using custom web-scraping scripts. For Devpost, data is fetched directly using the requests library, which retrieves hackathon information via API calls. The script handles pagination to gather data across multiple pages. Devfolio data is also extracted using API requests. Currently, we are working on scraping data from MLH.

## Data Processing
The scraped data is processed directly within the scripts by extracting relevant fields such as title, location, submission period dates, and URL. Since the data from Devpost and Devfolio is structured, no additional data cleaning steps are applied before it is saved in CSV format and used for display in the frontend.
