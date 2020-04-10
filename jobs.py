from bs4 import BeautifulSoup
from selenium import webdriver

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


def parse_jobs(jobs):
    jobs_parsed = []
    for count, job in enumerate(jobs):
        url = job['loc']
        while 'Title' not in job or not len(job['Title']):
            header = get_job_header(url)
            job['Title'] = get_job_title(header)
            job['Locations'] = get_job_locations(header)
        print(f"{count+1} loaded: {job['Title']} - {job['Locations']}")
        jobs_parsed.append(job)
    return jobs_parsed
