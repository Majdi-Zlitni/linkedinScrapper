import pickle
import init


class Cookies:
    def getCookies(self,driver):
        with open("linkedin_cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                # Modify the cookie's domain if necessary to match the current domain
                if 'domain' in cookie and cookie['domain'].startswith('.'):
                    cookie['domain'] = 'www.linkedin.com'
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Could not add cookie")

    def saveCookies(self,driver):
        cookies =driver.get_cookies()
        with open("linkedin_cookies.pkl", "wb") as file:
            pickle.dump(cookies, file)    
    
