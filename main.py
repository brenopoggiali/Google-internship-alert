from sitemap import get_jobs
from jobs import get_internships


def print_internships_by_country(internships):
    return


if __name__ == '__main__':
    print("Getting jobs...")
    jobs = get_jobs()
    print("Getting internships...")
    internships = get_internships(jobs)
    for internship in internships:
        print(internship)
    # print_internships_by_country(internships)
