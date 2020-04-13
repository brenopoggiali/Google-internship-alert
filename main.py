import os
from sitemap import get_jobs
from tabulate import tabulate
from jobs import get_internships, parse_jobs


def clean_screen():
    return os.system('cls' if os.name == 'nt' else 'clear')


def get_terminal_link(url):
    text = "Link"
    terminal_link = f"\u001b]8;;{url}\u001b\\{text}\u001b]8;;\u001b\\"
    return terminal_link


def get_countries(locations):
    countries = [i[0] for i in locations]
    countries = sorted(set(countries))
    return ', '.join(countries)


def print_internships(internships):
    table = []
    for internship in internships:
        url = internship['loc']
        title = internship['title']
        countries = get_countries(internship['locations'])
        link = get_terminal_link(url)
        table.append([title,  countries, link])
    table = sorted(table, key=lambda x: x[1])
    print(tabulate(table, headers=['Title', 'Countries', 'Link']))
    return


if __name__ == '__main__':
    print("Getting jobs...")
    jobs = get_jobs()
    internships_urls = get_internships(jobs)
    print(f"Parsing {len(internships_urls)} internships... ")
    internships = parse_jobs(internships_urls)
    clean_screen()
    print_internships(internships)