import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
 

from config import Configuration
from init import init

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
            if "…more" in post_content:
                more_button=post.find_element(By.XPATH, '//div/button/span[contains(text(),\'…more\')]')
                more_button.click()
                time.sleep(1)
                post_content_element = post.find_element(By.CLASS_NAME, 'feed-shared-update-v2__description')
                post_content = post_content_element.text

        except Exception as e:
            post_content = 'N/A'
        
        try:
            
            Additional_post_Link = post.find_element(By.CLASS_NAME, 'feed-shared-update-v2__description')
            post_content = post_content_element.text
            if "…more" in post_content:
                more_button=post.find_element(By.XPATH, '//div/button/span[contains(text(),\'…more\')]')
                more_button.click()
                time.sleep(1)
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
        pattern = r'[^a-zA-Z0-9]'
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
        
                
        for post in posts:
            user_name = post[0].replace(" ","")
            match = re.search(pattern, user_name)
            if match:
                user_name = user_name[:match.start()]            
            user_path=init.scrapped_data_folder_path+f"\\{user_name}"
            output_file_path = os.path.join(user_path, f'post_{user_name}.txt')
            os.makedirs(user_path, exist_ok=True)
            with open(output_file_path, 'w', encoding='utf-8') as file:
                user_job_or_followers = "Followers" if post[1].startswith(tuple("0123456789")) else "Job Title"
                file.write(f"User Name: {post[0]}\n")
                file.write(f"{user_job_or_followers}: {post[1]}\n")
                file.write(f"Profile Image URL: {post[2]}\n")
                file.write(f"Post Content: {post[3]}\n")
                file.write("-" * 40 + "\n")
                image_url = post[2]
                image_file_path = os.path.join(user_path, f'{user_name}.jpg')
                self.SaveImageToFolder(image_url,image_file_path)

            print("User Name:", post[0])
            print(f"{user_job_or_followers}:", post[1])
            print("Profile Image URL:", post[2])
            print("Post Content:", post[3])
            print("-" * 40)

    def SaveImageToFolder(self,image_url,image_file_path):
        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(image_file_path, 'wb') as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                print(f"Profile image saved to {image_file_path}")
            else:
                print(f"Failed to download image for")
        except Exception as e:
            print(f"An error occurred while downloading the image for: {e}")

    def collectDataFromGroup(self):
        self.driver.get(config.linkedInURLGroupURL) 
        self.collectAllPosts()