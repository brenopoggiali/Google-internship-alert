from sitemap import get_jobs
from jobs import get_internships, parse_jobs


def print_internships_by_country(internships):
    return


if __name__ == '__main__':
    print("Getting jobs...")
    jobs = get_jobs()
    internships_urls = get_internships(jobs)
    print(f"Parsing {len(internships_urls)} internships... ")
    internships = parse_jobs(internships_urls)
    # print_internships_by_country(internships)
