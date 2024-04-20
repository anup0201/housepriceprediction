import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from concurrent import futures
import json

mumbai_link_df = pd.read_csv("./data/property_links_Mumbai.csv")
navi_link_df = pd.read_csv("./data/property_links_Navi Mumbai.csv")

df = pd.concat([mumbai_link_df, navi_link_df])
list_of_dictionaries = []
list_of_errored_liks = []


# def extract_data_from_section_to_dict(
#     soup,
#     html_tag_type,
#     html_tag_class,
#     html_tag_name,
#     heading_html_class,
#     value_html_class,
#     heading_html_tag,
#     value_html_tag,
#     dictionary,
# ):
#     try:
#         details = soup.find_all(html_tag_type, {html_tag_class: html_tag_name})
#         list_headings = details[0].find_all(
#             heading_html_tag, {"class": heading_html_class}
#         )
#         list_values = details[0].find_all(value_html_tag, {"class": value_html_class})
#         for indice in range(len(list_headings)):
#             if list_headings[indice].text == "Carpet Area":
#                 dictionary[list_headings[indice].text] = list_values[indice].text.split(
#                     "sqft"
#                 )[0]
#             elif html_tag_name == "mb-ldp__dtls__body__summary":
#                 if any(char.isdigit() for char in list_headings[indice].text):
#                     dictionary[
#                         "".join(
#                             char
#                             for char in list_headings[indice].text
#                             if not char.isdigit()
#                         )
#                     ] = list_values[indice].text
#                 else:
#                     pass
#             else:
#                 dictionary[list_headings[indice].text] = list_values[indice].text
#     except IndexError:
#         pass

#     return dictionary


# def extract_data_from_link(row):
#     dictionary_of_details = {}
#     # Browser tasks automation to deal with js
#     browser = BrowserAutomate(row)
#     browser.setup_firefox()
#     time.sleep(3)
#     browser.click_view_all_details_and_amenities()
#     # get the page source to parse using beautiful soup
#     soup = BeautifulSoup(browser.driver.page_source, "html.parser")
#     dictionary_of_details["id"] = row.split("id=")[1]
#     # Grabbing details from summary section
#     dictionary_of_details = extract_data_from_section_to_dict(
#         soup,
#         html_tag_type="ul",
#         html_tag_class="class",
#         html_tag_name="mb-ldp__dtls__body__summary",
#         heading_html_tag="li",
#         heading_html_class="mb-ldp__dtls__body__summary--item",
#         value_html_tag="span",
#         value_html_class="mb-ldp__dtls__body__summary--highlight",
#         dictionary=dictionary_of_details,
#     )
#     # Grabbing the data from details section
#     dictionary_of_details = extract_data_from_section_to_dict(
#         soup,
#         html_tag_type="section",
#         html_tag_class="id",
#         html_tag_name="details",
#         heading_html_tag="div",
#         heading_html_class="mb-ldp__dtls__body__list--label",
#         value_html_tag="div",
#         value_html_class="mb-ldp__dtls__body__list--value",
#         dictionary=dictionary_of_details,
#     )
#     # Grabbing the data from more-details section
#     dictionary_of_details = extract_data_from_section_to_dict(
#         soup,
#         html_tag_type="section",
#         html_tag_class="id",
#         html_tag_name="more-details",
#         heading_html_tag="div",
#         heading_html_class="mb-ldp__more-dtl__list--label",
#         value_html_tag="div",
#         value_html_class="mb-ldp__more-dtl__list--value",
#         dictionary=dictionary_of_details,
#     )

#     amenities = soup.find_all("li", {"class": "mb-ldp__amenities__list--item"})
#     dictionary_of_details["Num of Amenities"] = len(amenities)
#     list_of_dictionaries.append(dictionary_of_details)

#     browser.driver.quit()
#     return dictionary_of_details


def getJson(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    soup = soup.find("div", attrs={"layout:fragment": "content"})
    result = soup.find_all("script")
    result = (
        result[0]
        .text.strip("\n")
        .strip("window.SERVER_PRELOADED_STATE_DETAILS =")
        .strip(";\n")
    )
    result = json.loads(result)
    list_of_dictionaries.append(result["propertyDetailInfoBeanData"]["propertyDetail"])
    return result


def process_row(row):
    try:
        return getJson(row)
    except Exception as e:
        list_of_errored_liks.append(row.split("id=")[1])
        print(e)
        return None


# Assuming df is your DataFrame and you want to process the "0" column
urls = df["0"].tolist()

# Using ThreadPoolExecutor to parallelize the task
with futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Map process_row function to all URLs
    results = list(executor.map(process_row, urls))

# Filter out None results in case of errors
results = [result for result in results if result is not None]

# Convert the list of dictionaries to a DataFrame
final_df = pd.DataFrame(results)
print(final_df)

# Save to CSV
final_df.to_csv("data/property_details.csv")
print(len(list_of_dictionaries))
print(len(list_of_errored_liks))


def function_a(msg):
    message = msg

    def function_b():
        print(msg)
        return function_b, msg + " return from function_a"


a, b = function_a("hello world")
print(a)
a()
print(b)
