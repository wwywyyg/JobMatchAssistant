from playwright.sync_api import sync_playwright
from scraper.job_scraper import scrape_jobs

def main():
    scrape_jobs()
    

if __name__ == "__main__":
    main()