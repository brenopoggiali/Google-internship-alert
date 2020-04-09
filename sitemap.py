import requests
import xmltodict

GOOGLE_SITEMAP_URL = "https://careers.google.com/jobs/sitemap"


def get_xml():
    response = requests.get(GOOGLE_SITEMAP_URL)
    jobs_data = xmltodict.parse(response.content)
    return jobs_data


def get_jobs():
    jobs_data = get_xml()
    jobs = jobs_data['urlset']['url']
    return jobs


# if __name__ == '__main__':
#     get_jobs()
