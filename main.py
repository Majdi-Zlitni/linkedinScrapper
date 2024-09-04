import init
from pages import feedsPage, loginPage


def main():
    initialize = init.init()
    driver= initialize.get_driver()
    login_page = loginPage.LoginPage(driver)
    feed_page= feedsPage.feedPage(driver)
    

    #try:
    login_page.loginToLinkedin()
    feed_page.collectAllPosts()
    feed_page.collectDataFromGroup()
    

if __name__ == "__main__":
    main()