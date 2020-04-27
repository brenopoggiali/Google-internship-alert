from bs4 import BeautifulSoup
from selenium import webdriver


def load_chrome():
    options = webdriver.ChromeOptions()
    options.headless = True
    browser = webdriver.Chrome(
        './browsers/chromedriver',
        chrome_options=options)
    return browser


def load_firefox():
    options = webdriver.FirefoxOptions()
    options.headless = True
    browser = webdriver.Firefox(
        executable_path='./browsers/firefoxdriver',
        options=options)
    return browser


def parse_html(browser):
    html = browser.page_source
    page = BeautifulSoup(html, 'html.parser')
    return page
