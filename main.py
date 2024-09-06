import init
from pages import feedsPage, loginPage, profilePage


def main():
    initialize = init.init()
    driver= initialize.get_driver()
    login_page = loginPage.LoginPage(driver)
    feed_page= feedsPage.feedPage(driver)
    profile_page= profilePage.profilePage(driver)
    

    login_page.loginToLinkedin()
    feed_page.collectAllPosts()
    feed_page.collectDataFromGroup()
    profile_page.collectDataFromUser()


    driver.quit()


if __name__ == "__main__":
    main()