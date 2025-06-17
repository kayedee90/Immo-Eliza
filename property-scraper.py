import pandas as pd
from parsel import Selector
from seleniumbase import Driver

# Function to extract locality from URL
def extract_locality(url):
    """ Extract the listing number from the URL. """
    return url.split("/")[-1]  # Gets the last part of the URL

class PropertyScraper:
    """ Create class to scrape the attributes of listed houses. """
    def __init__(self, url):
        self.url = url
        self.house_dict = {}  # Dictionary to store the attributes

        self.locality = extract_locality(self.url)  # Get listing number

        self.propertytype = None       #type of property (house or appartement)
        self.subtype = None            #Subtype of property (Bungalow, Chalet, Mansion, ...)
        self.price = None              #listed price of property
        self.saletype = None           #type of sale (Exclusion of life sales)
        self.rooms = None              #number of rooms
        self.area = None               #living area
        self.kitchen = 0               #furnished kitchen, 1 for yes 0 for no
        self.furnished = 0             #property comes fully furnished, 1 for yes 0 for no
        self.fire = 0                  #open fire, 1 for yes 0 for no
        self.terrace = 0               #terrace, 1 for yes 0 for no
        self.terrace_area = None       #terrace area if applicable
        self.garden = 0                #garden, 1 for yes 0 for no
        self.garden_area = None        #garden area if applicable
        self.surface = None            #surface area of the land
        self.surface_plot = None       #surface area of the plot
        self.facades = None            #the number of facades
        self.pool = 0                  #swimmingpool,1 for yes 0 for no
        self.building_state = None     #state of the building (new, to be renovated, ...)

    def fetch_page(self):
        """ Load property page and return parsed HTML. """
        driver = Driver(uc=True, headless=True)
        driver.get(self.url)
        sel = Selector(text=driver.page_source)
        driver.quit()
        return sel

    def extract_data(self, sel):
        """ Extract property details using XPath. Modify as needed. """
        self.propertytype = sel.xpath("//span[contains(@class, 'property-type')]/text()").get()
        self.subtype = sel.xpath("//span[contains(@class, 'subtype')]/text()").get()
        self.price = sel.xpath("//div[contains(@class, 'heading-2')]/text()").get()  # Updated XPath

        # Store processed values in dictionary
        self.house_dict = {
            "Listing Number": self.locality,
            "Property Type": self.propertytype,
            "Subtype": self.subtype,
            "Price": self.price
        }

    def scrape_details(self):
        """ Main method to scrape property details and store results. """
        sel = self.fetch_page()
        self.extract_data(sel)
        return self.house_dict


#load URLs from CSV file
df = pd.read_csv(r"Immo-Eliza\data\house_urls.csv")  # Adjust path if needed
house_urls = df["House URL"].tolist()

# Step 2: Iterate through each URL and scrape property details
scraped_data = []  # List to store results

for url in house_urls:
    scraper = PropertyScraper(url)
    data = scraper.scrape_details()
    scraped_data.append(data)

# Step 3: Save scraped data to a new CSV file
df_scraped = pd.DataFrame(scraped_data)
df_scraped.to_csv(r"Immo-Eliza\data\scraped_property_data.csv", index=False)

print(f"Saved {len(scraped_data)} property listings to 'property_data.csv'.")
