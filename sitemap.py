import xmltodict
from browsers import load_firefox

GOOGLE_SITEMAP_URL = "https://careers.google.com/jobs/sitemap"


def get_xml():
    browser = load_firefox()
    browser.get(GOOGLE_SITEMAP_URL)
    jobs_data = xmltodict.parse(browser.page_source)
    browser.quit()
    return jobs_data


def get_jobs():
    jobs_data = get_xml()
    jobs = jobs_data['urlset']['url']
    return jobs


def get_internships(jobs):
    internships = []
    for job in jobs:
        url = job['loc']
        mid = '-intern-' in url
        end = '-intern/' in url
        if mid or end:
            internships.append(job)
    return internships
