
import requests
import pandas as pd
from parsel import Selector
from seleniumbase import Driver

# define base URL
base_url = "https://www.immoscoop.be"

# initialize undetected selenium driver, headless to run browser in background
driver = Driver(uc=True, headless=True)

# store house url's
houses_url = []

# loop through multiple result pages
for number in range(1, 5):  # Fetch up to page x (adjust as needed)
    url = f"{base_url}/search/for-sale?page={number}"
    
    driver.get(url)  # load search results page
    sel = Selector(text=driver.page_source)  # parse page source
    
    # find house links using xpath
    xpath_houses = "//div[@class='will-change-transform']/a/@href"
    page_houses_url = sel.xpath(xpath_houses).getall()
    
    if page_houses_url:  # add only non-empty results
        houses_url.extend(page_houses_url)

driver.quit()  # close background browser

print(f"Total houses found: {len(houses_url)}")

# create full url's to ensure proper storage
full_houses_url = [base_url + url for url in houses_url]

# Store url's in csv
df = pd.DataFrame(full_houses_url, columns=["House URL"])
df.to_csv(r"Immo-Eliza\data\house_urls.csv", index=False)
print(f"Saved {len(full_houses_url)} house URLs to 'house_urls.csv'")


