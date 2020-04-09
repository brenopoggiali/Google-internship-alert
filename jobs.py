import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions \
    import presence_of_element_located


HEADER_CLASS = 'gc-card__header gc-job-detail__header'


def load_browser():
    options = webdriver.firefox.options.Options()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options=options)
    return browser


def get_page(job_url):
    browser = load_browser()
    browser.get(job_url)
    return browser


def parse_html(browser):
    html = browser.page_source
    page = BeautifulSoup(html, 'html.parser')
    browser.quit()
    return page


def get_job_header(url):
    browser_page = get_page(url)
    page = parse_html(browser_page)
    header = page.find('div', {'class': HEADER_CLASS})
    return header


def get_job_title(header):
    title = header.find('h1')
    return title.text


def get_job_locations(header):
    locations = []
    for div in header.find_all('div', itemprop='address'):
        city = div.find('div', itemprop="addressLocality")
        if city:
            city = city.text.strip()

        state = div.find('div', itemprop="addressRegion")
        if state:
            state = state.text.strip()

        country = div.find('div', itemprop="addressCountry")
        if country:
            country = country.text.strip()

        location = [country, state, city]
        locations.append(location)
    return locations


def get_internships(jobs):
    internships = []
    count = 0
    for job in jobs:
        url = job['loc']
        if 'intern' in url:
            count += 1
            header = get_job_header(url)
            if header is None:
                continue
            job['Title'] = get_job_title(header)
            job['Locations'] = get_job_locations(header)
            print(f"Found {count} internships - {job['Title']} - {url}")
            internships.append(job)
    return internships
