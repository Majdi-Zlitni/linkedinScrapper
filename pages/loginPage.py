# pages/login_page.py

import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import Configuration
from utils.cookies import Cookies
from utils.browserHelper import BrowserHelper;


config=Configuration()
cookies=Cookies()

class LoginPage:
    
    def __init__(self, driver, cookies_file="linkedin_cookies.pkl"):
        self.driver = driver
        self.cookies_file = cookies_file        
                        

    def enter_username(self, username):
        self.driver.find_element(By.ID, "username").send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(By.ID, "password").send_keys(password)

    def click_login_button(self):
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()    
        
    def loginToLinkedin(self):
        if os.path.exists(self.cookies_file):
            cookies.getCookies(self.driver)
            self.driver.get(config.linkedInFeedURL) 
            if BrowserHelper.element_exists(self,By.ID, "password"):
                os.remove(self.cookies_file)  
                self.loginToLinkedin()          
            return             
        self.enter_username(config.email)
        self.enter_password(config.password)
        self.click_login_button()   
        cookies.saveCookies(self.driver) 
