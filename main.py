import pandas as pd
from parsel import Selector
from Immo_Eliza.property_scraper import PropertyScraper

# Load URLs from CSV file.
df = pd.read_csv(r"Immo_Eliza\data\house_urls.csv")   # Adjust path if needed
house_urls = df["House URL"].tolist()


scraped_data = []  # To store the results

for url in house_urls:
    scraper = PropertyScraper(url)
    data = scraper.scrape_details()
    if data:
        scraped_data.append(data)

# Save the scraped data to CSV.
df_scraped = pd.DataFrame(scraped_data)
df_scraped.to_csv(r"Immo_Eliza\data\property_data.csv", index=False)
print(f"Saved {len(scraped_data)} property listings to 'property_data.csv'.")
