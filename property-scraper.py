import pandas as pd
import requests
from parsel import Selector

def extract_locality(url):
    """Extract the listing number from the URL."""
    return url.split("/")[-1]  # Gets the last part of the url

class PropertyScraper:
    """class to scrape property details"""
    def __init__(self, url):
        self.url = url
        self.house_dict = {}  # Dictionary to store the attributes

        self.locality = extract_locality(self.url)  # Listing number

        # Initialize attributes
        self.propertytype = None       # House or Apartment
        self.subtype = None            # Bungalow, Chalet, etc.
        self.price = None              # Listed price
        self.buildyear = None          # year the property was built
        self.renovationyear = None     # year the building was renovated
        self.rooms = None              # Number of rooms
        self.area = None               # Living area
        self.epc = None                # EPC value
        self.garage = None             # Garage?
        self.terrace = None            # Terrace?
        self.terrace_area = None       # Terrace area
        self.garden = None             # Garden?
        self.garden_area = None        # Garden area
        self.surface_plot = None       # Plot surface area
        self.facades = None            # Number of facades
        


    def fetch_page(self):
        """Load property page using requests."""
        headers = {"User-Agent": "Mozilla/5.0"} # Prevent blocking by mimicking browser
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            return Selector(text=response.text)
        else:
            return None

    def extract_data(self, sel):
        """
        Extract property details using XPath selectors.
        """
        self.propertytype = sel.xpath("//div[@class='container-fluid grid grid-cols-1 gap-8 py-6 md:grid-cols-2 lg:grid-cols-3']//div[2]//div[1]//div[1]//div[2]//div[1]/text()").get()
        self.subtype = sel.xpath("//div[@class='container-fluid grid grid-cols-1 gap-8 py-6 md:grid-cols-2 lg:grid-cols-3']//div[2]//div[1]//div[2]//div[2]//div[1]/text()").get()
        self.price = sel.xpath("//div[@class='heading-2 mb-2']/text()").get()
        self.buildyear = sel.xpath("/text()").get()
        self.renovationyear = sel.xpath("//div[@class='container-fluid grid grid-cols-1 gap-8 py-6 md:grid-cols-2 lg:grid-cols-3']//div[2]//div[1]//div[2]//div[2]//div[1]/text()").get()
        self.rooms = sel.xpath("//div[contains(@class, 'grid-cols-1')]//div[2]/div/div[2]/div[5]/div/div[1]/div[2]/div/text()").get()
        self.area = sel.xpath("//div[contains(text(),'168 m²')]/text()").get()
        self.epc = sel.xpath("/text()").get()
        self.garage = sel.xpath("/text()").get()
        self.terrace = sel.xpath("//div[4]//div[1]//div[4]//div[2]//div[1]/text()").get()
        self.terrace_area = sel.xpath("//div[contains(text()]/text()").get()
        self.garden = sel.xpath("//div[3]//div[1]//div[3]//div[2]//div[1]/text()").get()
        self.garden_area = sel.xpath("//div[contains(text(),'250 m²')]/text()").get()
        self.surface_plot = sel.xpath("//div[contains(text(),'364 m²')]/text()").get()
        self.facades = sel.xpath("//div[@class='container-fluid grid grid-cols-1 gap-8 py-6 md:grid-cols-2 lg:grid-cols-3']//div[1]/div/div/main/div[2]/div/div/div[2]/div/div[6]/div[2]/div").get()

        # Build the final dictionary.
        self.house_dict = {
            "Listing Number": self.locality,
            "Property Type": self.propertytype,
            "Subtype": self.subtype,
            "Price": self.price,
            "Build Year": self.buildyear,
            "Renovation Year": self.renovationyear,
            "Number of Rooms": self.rooms,
            "Living Area": self.area,
            "EPC Value": self.epc,
            "Garage": self.garage,
            "Terrace": self.terrace,
            "Terrace Size": self.terrace_area,
            "Garden": self.garden,
            "Garden Size": self.garden_area,
            "Plot Surface Area": self.surface_plot,
            "Facades": self.facades,
        }

    def scrape_details(self):
        """Fetch page and extract property details."""
        sel = self.fetch_page()
        if sel:
            self.extract_data(sel)
        return self.house_dict



# ----- Execution Section -----



# Load URLs from CSV file.
df = pd.read_csv(r"Immo-Eliza\data\house_urls.csv")   # Adjust path if needed
house_urls = df["House URL"].tolist()[:5] # Set to 5 for code testing


scraped_data = []  # To store the results

for url in house_urls:
    scraper = PropertyScraper(url)
    data = scraper.scrape_details()
    if data:
        scraped_data.append(data)

# Save the scraped data to CSV.
df_scraped = pd.DataFrame(scraped_data)
df_scraped.to_csv(r"Immo-Eliza\data\property_data.csv", index=False)
print(f"Saved {len(scraped_data)} property listings to 'property_data.csv'.")

#Display first few rows.
df_result = pd.read_csv(r"Immo-Eliza\data\property_data.csv")
print(df_result.head())