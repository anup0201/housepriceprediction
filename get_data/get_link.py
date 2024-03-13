# Import the required libraries
import requests
from bs4 import BeautifulSoup
from browser_automate import BrowserAutomate
import json
import pandas as pd
from tqdm import tqdm


def url_format(city):
    # The URL of the website
    url_to_request = f"https://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=1,4,5,%3E5,2,3&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&cityName={city}"
    return url_to_request


def get_list_from_site(loaded_html, cityName):
    soup = BeautifulSoup(loaded_html, "html.parser")
    # Find all <div> tags with class="mb-srp__list"
    data_div = soup.find_all("div", {"class": "mb-srp__list"})
    # create a blank series
    link_series = []
    print(len(data_div))
    # get the url to property from the script tag within the div class
    for data_item in tqdm(data_div):
        script_tags = data_item.find_all("script", {"type": "application/ld+json"})
        json_data = json.loads(script_tags[0].text)
        try:
            link_series.append(json_data["url"])
        except KeyError:
            pass
    link_series = pd.Series(link_series)
    link_series.to_csv(f"data/property_links_{cityName}.csv", index=False)


cityName = "Navi Mumbai"
url = url_format(cityName)
browser = BrowserAutomate(url)
browser.scroll_page()
browser.driver.implicitly_wait(10)

# Now, we fetch the complete loaded page HTML
complete_loaded_page_html = browser.driver.page_source

# Close the driver
browser.driver.quit()

get_list_from_site(complete_loaded_page_html, cityName)
