import pandas as pd
import requests
from parsel import Selector

def extract_locality(url):
    """Extract the listing number from the URL."""
    return url.split("/")[-1]  # Gets the last part of the url

class PropertyScraper:
    """
    Define property scraper class
    """
    def __init__(self, url):
        self.url = url
        self.house_dict = {}

        self.locality = extract_locality(self.url)
        #set attributes to none for error handling
        self.propertytype = None
        self.subtype = None
        self.price = None
        self.rooms = None
        self.area = None
        self.epc = None
        self.epc_label = None  
        self.garden = None
        self.surface_plot = None

    def fetch_page(self):
        headers = {"User-Agent": "Mozilla/5.0"} # Mimic user activity
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            return Selector(text=response.text)
        return None

    def extract_data(self, sel):
        features = {}
        


        label_elements = sel.xpath("//div[contains(@class, 'feature-values_component_label__')]")
        for label_elem in label_elements:
            label = label_elem.xpath("text()").get()
            value = label_elem.xpath(
                "following-sibling::div[contains(@class, 'feature-values_component_value__')][1]"
                "//div[contains(@class, 'feature-values_component_valueContent__')]/text()"
            ).get()
            if label and value:
                features[label.strip()] = value.strip()

        self.propertytype = features.get("Type of property")
        self.subtype = features.get("Subtype") or features.get("Property subtype")
        self.price = sel.xpath("//div[contains(@class, 'heading-2')]/text()").get()
        self.rooms = features.get("Number of bedrooms")
        self.area = features.get("Living area") or features.get("Surface")
        self.epc = features.get("EPC score") or features.get("EPC score (kWh/(m² years))")
        self.epc_label = features.get("EPC label")
        self.garden = features.get("Garden")
        self.surface_plot = features.get("Plot size") or features.get("Land area")

        self.house_dict = {
            "Listing Number": self.locality,
            "Property Type": self.propertytype,
            "Subtype": self.subtype,
            "Price": self.price,
            "Number of Rooms": self.rooms,
            "Living Area": self.area,
            "EPC Value": self.epc,
            "EPC Label": self.epc_label,
            "Garden": self.garden,
            "Plot Surface Area": self.surface_plot,
        }

    def scrape_details(self):
        sel = self.fetch_page()
        if sel:
            self.extract_data(sel)
            # Filter op type property
            if self.propertytype and self.propertytype.lower() in ['house', 'appartement', 'apartment']:
                return self.house_dict
        return None
    
