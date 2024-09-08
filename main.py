import init
from pages import feedsPage, loginPage, profilePage


def main():
    initialize = init.init()
    driver= initialize.get_driver()
    login_page = loginPage.LoginPage(driver)
    feed_page= feedsPage.FeedPage(driver)
    profile_page= profilePage.ProfilePage(driver)
    

    login_page.loginToLinkedin()
    feed_page.collect_all_posts()
    #feed_page.collect_data_from_group()
    #profile_page.collectDataFromUser()


    driver.quit()


if __name__ == "__main__":
    main()