import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import Configuration

config=Configuration()
class feedPage:
    def __init__(self, driver):
        self.driver = driver
    

    def extractPostDetails(self,post):
        try:
            name_element = post.find_element(By.CLASS_NAME, 'update-components-actor__name')
            user_name = name_element.text
        except Exception as e:
            user_name = 'N/A'

        try:
            job_title_element = post.find_element(By.CLASS_NAME, 'update-components-actor__description')
            job_title = job_title_element.text
        except Exception as e:
            job_title = 'N/A'

        try:
            profile_image_element = post.find_element(By.CSS_SELECTOR, 'img.update-components-actor__avatar-image')
            profile_image_url = profile_image_element.get_attribute('src')
        except Exception as e:
            profile_image_url = 'N/A'

        try:
            post_content_element = post.find_element(By.CLASS_NAME, 'feed-shared-update-v2__description')
            post_content = post_content_element.text
        except Exception as e:
            post_content = 'N/A'

        return user_name, job_title, profile_image_url, post_content
        

    def collectAllPosts(self):
        # Scroll and scrape posts
        scroll_pause_time = 3
        posts = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Find all posts on the current page
            post_elements = self.driver.find_elements(By.CLASS_NAME, 'feed-shared-update-v2')            
            if not post_elements:
                break
            
            for post in post_elements:
                post_details = self.extractPostDetails(post)
                posts.append(post_details)
            
            # Scroll down to load more posts
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)  # Wait for posts to load

            # Calculate new scroll height and compare with the last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Print all collected posts
        for post in posts:
            print("User Name:", post[0])
            print("Job Title:", post[1])
            print("Profile Image URL:", post[2])
            print("Post Content:", post[3])
            print("-" * 40)

    def collectDataFromGroup(self):
        self.driver.get(config.linkedInURLGroupURL) 
        self.collectAllPosts()