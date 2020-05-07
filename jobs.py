from browsers import load_chrome, parse_html

HEADER_CLASS = 'gc-card__header gc-job-detail__header'


def load_tabs(browser, jobs):
    tabs = []
    for idx, job in enumerate(jobs):
        arg = f"window.open('{job['loc']}', 'tab{idx+1}');"
        browser.execute_script(arg)
        tabs.append(f'tab{idx+1}')
    return tabs


def get_job_header(page):
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


def is_job_open(page):
    closed_message = 'Applications are currently closed for this role.'
    if closed_message in str(page):
        return 'Closed'
    return 'Open'


def process_job(browser):
    job = {}
    while 'title' not in job or not len(job['title']):
        page = parse_html(browser)
        header = get_job_header(page)
        if header is None:
            continue
        job['title'] = get_job_title(header)
        job['locations'] = get_job_locations(header)
        job['valid'] = is_job_open(page)
        job['url'] = browser.current_url
    print(f"Loaded: {job['title']} - {job['locations']}")
    return job


def process_jobs(browser, tabs):
    jobs_parsed = []
    for tab in tabs:
        browser.switch_to.window(tab)
        jobs_parsed.append(process_job(browser))
    return jobs_parsed


def parse_jobs(jobs):
    browser = load_chrome()
    tabs = load_tabs(browser, jobs)
    jobs_parsed = process_jobs(browser, tabs)
    browser.quit()
    return jobs_parsed
