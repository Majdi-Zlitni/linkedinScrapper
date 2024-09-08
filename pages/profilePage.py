import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import Configuration

config=Configuration()
class ProfilePage:
    def __init__(self, driver):
        self.driver = driver
        
    def collectDataFromUser(self):
        self.driver.get(config.linkedInUserURL)    
        info=self.extractUserData()
        print("User Name:", info[0])
        print("Job Title:", info[1])
        print("Profile Image URL:", info[2])           
        print("-" * 40)


    def extractUserData(self):
        try:
            name_element = self.driver.find_element(By.XPATH, '//h1[@class=\'text-heading-xlarge inline t-24 v-align-middle break-words\']')
            user_name = name_element.text
        except Exception as e:
            user_name = 'N/A'

        try:
            job_title_element = self.driver.find_element(By.XPATH, '//div[@class=\'text-body-medium break-words\']')
            job_title = job_title_element.text
        except Exception as e:
            job_title = 'N/A'

        try:
            profile_image_element = self.driver.find_element(By.XPATH, '//img[contains(@id, \'ember\') and contains(@class, \'ESdLmyrnbX\')]')
            profile_image_url = profile_image_element.get_attribute('src')
        except Exception as e:
            profile_image_url = 'N/A'
        
        return user_name, job_title, profile_image_url