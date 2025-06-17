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

