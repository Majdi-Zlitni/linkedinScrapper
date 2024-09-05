# LinkedIn Scraper Project

This project is a LinkedIn scraping tool built using Python and Selenium, designed to automate various LinkedIn tasks, such as scraping the news feed, extracting posts and scraping data from groups.

## Features

- **Login Automation**: Automates the login process to LinkedIn using Selenium and using extracted coockies.
- **Feed Scraping**: Extracts posts from your LinkedIn feed.
- **Post Scraping**: Scrapes posts from individual user profiles.
- **Group Data Extraction**: Retrieves data from LinkedIn groups.

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/LinkedInScraper.git
```

2. Navigate to the project directory:

```
cd LinkedInScraper
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

4. If the provided chromedriver version is not compatible with your chrome browser download the appropriate version and place it in the webDriver directory. You can download it from [here](https://googlechromelabs.github.io/chrome-for-testing/).

### Important Setup Notes

1. **Config File**:
   Ensure that the `config` file, where your LinkedIn credentials and other configurations are stored, has the `.py` extension (i.e., `config.py`). Place it inside the `LinkedInScraper` folder.

2. **Cookie Storage**:
   The LinkedIn cookies will be saved and reused to avoid logging in every time. Place the `linkedin_cookies.pkl` file in the `LinkedInScraper` folder. This file will be automatically created after the first successful login. Make sure you have the file in place before running scripts that require LinkedIn authentication.

## Running main file

Run the Python file from the command line or terminal:

```
python main.py
```

## Project Structure

```plaintext
/LinkedInScraper
│
│
├── /webDriver
│   └── chromedriver.exe  # WebDriver executables
│
├── /pages
│   ├── login_page.py  # Login Page Object Model
│   └── feed_page.py  # Feed Scraper
│
├── /utils
│   └── cookies.py  # File that contain linkedin user coockies
│
├── config.py  # Configuration like URLs, credentials, etc.
├── requirements.txt.py  # requirement file.
├── linkedin_cookies.pkl  # Python dependencies
├── README.md  # Read me file
├── init.py  # File to initialize variables
└── main.py  # Main script to run tests
```
