from selenium import webdriver
from selenium.webdriver.common.by import By

import time
from tqdm import tqdm
import logging


class BrowserAutomate:
    def __init__(self, url):
        self.url = url
        self.required_repetitions = 55  # extra scrolls so that nothing gets missed.
        self.setup_firefox()

    def setup_firefox(self):
        # Setup Firefox options
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")  # Ensure GUI is off
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("window-size=1920x1080")
        firefox_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
        )

        # Choose Firefox Browser
        self.driver = webdriver.Firefox(options=firefox_options)

        self.driver.get(self.url)

    # Function to simulate scrolling
    def scroll_page(self):
        SCROLL_PAUSE_TIME = 10  # Pause time between scrolls

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Setup logging
        logging.basicConfig(
            filename="scroll_log.log",
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
        )

        logging.info(f"Scrolling initiated for {self.url}")
        for i in tqdm(range(self.required_repetitions)):
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            # Log each scroll
            logging.info(f"Scrolled {i+1} times")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
        logging.info("Completed scrolling through the page.")

    def click_view_all_details_and_amenities(self):
        try:
            # Find and click the "View all Details" button
            details_button = self.driver.find_element(
                By.CLASS_NAME, "mb-ldp__more-dtl--viewall"
            )
            details_button.click()
        except Exception as e:
            pass

        try:
            # Find and click the "View all Amenities" button
            amenities_button = self.driver.find_element(
                By.CLASS_NAME, "mb-ldp__amenities--viewall"
            )
            amenities_button.click()
        except Exception as e:
            pass
