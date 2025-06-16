import requests
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver

# Website URL
url = "https://www.immoscoop.be/en/"

# Initialize undetected Chrome driver
driver = Driver(uc=True)
driver.get(url)

# Wait for cookie to be clickable
cookie_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All Cookies')]")))
driver.execute_script("arguments[0].click();", cookie_button)
print("Cookie clicked")
driver.close()


# API Request to Fetch Listings
house_url = "https://www.immoscoop.be/en/search/for-sale"

payload = {
    "transactionType": "Sale",
    "pageNumber": 1,
    "pageSize": 25,
}

headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36",
    "Referer": "https://www.immoscoop.be/",
    "Origin": "https://www.immoscoop.be/",
}

r = requests.post(url, json=payload, headers={ ... })
print(f"Status code: {r.status_code}")
print(f"Response text: {r.text}")  # Inspect raw response
r.raise_for_status()  # Ensure request succeeded
data = r.json()

# Extract listings and normalize to a DataFrame
ads = data.get("results", [])  # Adjust key based on actual API response
df = pd.json_normalize(ads)

# Preview extracted data
print(df.columns)
print(df[["property.title", "property.price.mainValue", "property.location.city"]].head())