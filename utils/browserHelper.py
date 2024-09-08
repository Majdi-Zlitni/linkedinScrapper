from selenium.common.exceptions import NoSuchElementException

class BrowserHelper:
        def __init__(self, driver):
            self.driver = driver
               
        def element_exists(self, by, value):
            try:
                self.driver.find_element(by, value)
                return True
            except NoSuchElementException:
                return False