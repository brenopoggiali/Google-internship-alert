import os
from jobs import parse_jobs
from tabulate import tabulate
from sitemap import get_jobs, get_internships


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
        url = internship['url']
        title = internship['title']
        countries = get_countries(internship['locations'])
        valid = internship['valid']
        link = get_terminal_link(url)
        table.append([title,  countries, valid, link])
    table = sorted(table, key=lambda x: ([-ord(c) for c in x[2]], x[1]))
    print(tabulate(table, headers=['Title', 'Countries', 'Status', 'Link']))
    return


def main():
    print("Getting jobs...")
    jobs = get_jobs()
    internships_urls = get_internships(jobs)
    print(f"Parsing {len(internships_urls)} internships... ")
    internships = parse_jobs(internships_urls)
    clean_screen()
    print_internships(internships)


if __name__ == '__main__':
    main()
