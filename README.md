# Immo-Eliza

Immo Eliza is a Python project using web scraping to create a dataset of Belgian real estate sales data.  
This project is a first step to building a machine learning project that can predict house prices.


# Context
I used immoscoop real estate company and looked for properties for sale across Belgium.

Currently, the program attempts to pull the following information (stored in the dataset):

Locality  
Type of property (House/apartment)  
Subtype of property (Bungalow, Chalet, Mansion, ...)  
Price   
Number of bedrooms
Living Area  
EPC Value
EPC Label
Garden (Yes/No)  
Surface area of the plot of land   


# Usage

Use link_scraper.py to scrape your desired amount of links.  
These links are then stored to house_urls.csv in the data folder.  
Next, run the immo_scraper, which pulls the links from the datafolder, scrapes the requested data, and stores it in property_data.csv in the datafolder.
