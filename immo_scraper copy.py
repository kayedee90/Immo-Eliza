import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
#website url
url = "https://www.immoscoop.be/"
#initialize undetected Chrome driver
driver = Driver(uc=True)
driver.get(url)
#wait for cookie to be clickable using the successful XPath selector
cookie_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aanvaard alle cookies')]")))
#use JavaScript to force the click
(driver.execute_script("arguments[0].click();", cookie_button))
print("Cookie clicked")
# Instead of closing the browser, wait for user input
input("Press Enter to close the browser")
driver.quit()