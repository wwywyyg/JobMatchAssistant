from playwright.sync_api import sync_playwright
from scraper.job_scraper import scrape_jobs

def main():
    jobs = scrape_jobs()

    print("\nResults")
    print("=" * 50)
    for(job) in jobs:
        print("Title:", job["title"])
        print("Company:", job["company"])
        print("Location:", job["location"])
        print("Description:", job["description"])
        print("posted at:", job["posted"])
        print("=" * 50)
    

if __name__ == "__main__":
    main()