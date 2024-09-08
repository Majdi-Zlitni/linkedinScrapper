import os
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import Configuration
from init import init
from utils.utils import utilities
from utils.browserHelper import BrowserHelper


# Define XPaths for different types of posts
xpath_pdf_post_link = '//div[contains(@class,\'ssplayer-virus-scan-container\')and text()]/a[contains(@href,\'https\')]'
xpath_image_post_link = '//div[contains(@class,\'ivm-view-attr__img-wrapper\')]/img[@width=\'600\']'
xpath_video_post_link = '//video[@class=\'vjs-tech\']'
xpath_max_button='//button[@class=\'ssplayer-fullscreen-on-button\']//li-icon'

config = Configuration()

class FeedPage:
    def __init__(self, driver):
        self.driver = driver

    def collect_all_posts(self):
        """Scroll and scrape posts."""
        scroll_pause_time = 3
        posts = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        pattern = r'[^a-zA-Z0-9]'
        post_number=1
        while True:
            post_elements = self.driver.find_elements(By.CLASS_NAME, 'feed-shared-update-v2')
            if not post_elements:
                break

            for post in post_elements:                
                post_details = self.extract_post_details(post,post_number)
                posts.append(post_details)
                post_number+=1
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        self.save_posts(posts, pattern)

    def CheckExistedElement(self,element_xpath):
        return BrowserHelper.element_exists(self,By.XPATH, element_xpath)        

    def extract_post_details(self, post,post_number):
        """Extract details from a single post."""
        image_post_content='N/A'
        video_post_content='N/A'
        pdf_post_content='N/A'

        user_name = self.get_element_text(post, By.CLASS_NAME, 'update-components-actor__name')
        job_title = self.get_element_text(post, By.CLASS_NAME, 'update-components-actor__description')
        profile_image_url = self.get_element_attribute(post, By.CSS_SELECTOR, 'img.update-components-actor__avatar-image', 'src')
        post_content = self.get_post_content(post)
        image_post_content= self.get_url_content(post,xpath_image_post_link,'src') 
        video_post_content=self.get_url_content(post, xpath_video_post_link, 'src')
        pdf_post_content=self.get_pdf_url_content(post, xpath_pdf_post_link, 'href')


        return user_name, job_title, profile_image_url, post_content, image_post_content, video_post_content, pdf_post_content

    def get_element_text(self, post, by, value):
        """Get text from an element."""
        try:
            element = post.find_element(by, value)
            return element.text
        except Exception:
            return 'N/A'

    def get_element_attribute(self, post, by, value, attribute):
        """Get attribute value from an element."""
        try:
            element = post.find_element(by, value)
            return element.get_attribute(attribute)
        except Exception:
            return 'N/A'

    def get_post_content(self, post):
        """Get the content of a post, including expanded content if available."""
        try:
            post_content_element = post.find_element(By.CLASS_NAME, 'feed-shared-update-v2__description')
            post_content = post_content_element.text
            if "…more" in post_content:
                more_button = post.find_element(By.XPATH, '//div/button/span[contains(text(),\'…more\')]')
                more_button.click()
                time.sleep(1)
                post_content_element = post.find_element(By.CLASS_NAME, 'feed-shared-update-v2__description')
                post_content = post_content_element.text
            return post_content
        except Exception:
            return 'N/A'

    def get_url_content(self, post, element_xpath, attribute):
        """Get URL content from a post."""
        try:
            if self.CheckExistedElement(element_xpath):
                element = post.find_element(By.XPATH, element_xpath)
                time.sleep(1)
            #self.driver.send_keys(Keys.ESCAPE)
                return element.get_attribute(attribute)
            return 'N/A'
        except Exception:
            return 'N/A'    

    def get_pdf_url_content(self, post, element_xpath, attribute):
        """Get URL content from a post."""
        try:
            if self.CheckExistedElement(element_xpath):
                post.click(xpath_max_button)
                element = post.find_element(By.XPATH, element_xpath)
                time.sleep(1)
            #self.driver.send_keys(Keys.ESCAPE)
                return element.get_attribute(attribute)
            return 'N/A'
        except Exception:
            return 'N/A'    

    def save_posts(self, posts, pattern):
        """Save posts to files."""
        for post in posts:
            user_name = re.sub(pattern, '', post[0].replace(" ", ""))
            user_path = os.path.join(init.scrapped_data_folder_path, user_name)
            output_file_path = os.path.join(user_path, f'post_{user_name}.txt')
            os.makedirs(user_path, exist_ok=True)

            with open(output_file_path, 'w', encoding='utf-8') as file:
                user_job_or_followers = "Followers" if post[1].startswith(tuple("0123456789")) else "Job Title"
                file.write(f"User Name: {post[0]}\n")
                file.write(f"{user_job_or_followers}: {post[1]}\n")
                file.write(f"Profile Image URL: {post[2]}\n")
                file.write(f"Post: {post[3]}\n")            
                file.write("-" * 40 + "\n")

                profile_image_url = post[2]
                image_post_url=post[4]
                video_post_url=post[5]
                pdf_post_url=post[6]
                image_file_path = os.path.join(user_path, f'{user_name}.jpg')     

                post_to_save, post_file_path = (
                    (image_post_url, os.path.join(user_path, f'{user_name}.jpg')) if image_post_url != 'N/A' else
                    (video_post_url, os.path.join(user_path, f'{user_name}.mp4')) if video_post_url != 'N/A' else
                    (pdf_post_url, os.path.join(user_path, f'{user_name}.pdf')) if pdf_post_url != 'N/A' else
                    (None, None))
                utilities.save_file_to_folder(profile_image_url, image_file_path)
                if post_to_save:
                    utilities.save_file_to_folder(post_to_save,post_file_path)

            print(f"User Name: {post[0]}")
            print(f"{user_job_or_followers}: {post[1]}")
            print(f"Profile Image URL: {post[2]}")
            print(f"Post Content: {post[3]}")
            print("-" * 40)

    def collect_data_from_group(self):
        """Collect data from a LinkedIn group."""
        self.driver.get(config.linkedInURLGroupURL)
        self.collect_all_posts()