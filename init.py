from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config
config=config.Configuration()

class init():
    chrome_driver_path = "./webDriver/chromedriver.exe"
    options = webdriver.ChromeOptions()    
    

    def __init__(self):
        try:
            self.driver = webdriver.Chrome(service=Service(self.chrome_driver_path), options=self.options)
            self.driver.maximize_window()
            self.driver.get(config.linkedInFeedURL)            

        except Exception as e:
            print(f"Error initializing Chrome WebDriver: {e}")
            self.driver = None
     
    def get_driver(self):
        return self.driver
