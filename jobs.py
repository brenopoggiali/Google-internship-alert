from bs4 import BeautifulSoup
from selenium import webdriver
from joblib import Parallel, delayed

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
    for job in jobs:
        url = job['loc']
        mid = '-intern-' in url
        end = '-intern/' in url
        if mid or end:
            internships.append(job)
    return internships


def process_job(job):
    url = job['loc']
    while 'title' not in job or not len(job['title']):
        header = get_job_header(url)
        job['title'] = get_job_title(header)
        job['locations'] = get_job_locations(header)
    print(f"Loaded: {job['title']} - {job['locations']}")
    return job


def parse_jobs(jobs):
    jobs_parsed = Parallel(n_jobs=-1)(delayed(process_job)(j) for j in jobs)
    return jobs_parsed
