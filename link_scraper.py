import pandas as pd
from parsel import Selector
from seleniumbase import Driver
import concurrent.futures


# define base URL
base_url = "https://www.immoscoop.be"

def fetch_house_urls(page_number):
    """
    function to fetch url's
    """
    url = f"{base_url}/en/search/for-sale?page={page_number}" #define the link for each page to search though
    driver = Driver(uc=True, headless=True) #use undetected selenium + run headless so browsers dont pop up
    driver.get(url)
    sel = Selector(text=driver.page_source)
    xpath_houses = "//div[@class='will-change-transform']/a/@href" #define the pathway to the houses
    page_houses_url = sel.xpath(xpath_houses).getall() #get the houses from the pathway and store them in the variable
    driver.quit()
    return page_houses_url

if __name__ == '__main__':
    total_pages = 100 #number of pages to be scraped
    houses_url = [] #dictionary to store pages

    #run multiple concurrent processes to speed up results
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor: #adjust workers if needed
        results = executor.map(fetch_house_urls, range(1, total_pages + 1))
        for page_urls in results:
            if page_urls:
                houses_url.extend(page_urls)

    #print number of houses found for easy overview
    print(f"Total houses found: {len(houses_url)}")


    # create full url's to ensure proper storage
    full_houses_url = [base_url + url for url in houses_url]
    # Store url's in csv
    df = pd.DataFrame(full_houses_url, columns=["House URL"])
    df.to_csv(r"Immo_Eliza\data\house_urls.csv", index=False)
    #print storage location
    print(f"Saved {len(full_houses_url)} house URLs to 'house_urls.csv'")


