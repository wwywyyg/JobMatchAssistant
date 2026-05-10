from playwright.sync_api import sync_playwright

def scrape_jobs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://realpython.github.io/fake-jobs/")

        page.wait_for_timeout(3000)

        # locate job content
        job_card = page.locator(".card-content")
        
        count = job_card.count()

        print(f"{count} jobs found\n")

        # iterate through first 5  jobs and extract job information 
        # page.pause()
        print("=" * 50)
        for i in range(min(count,20)):
            card = job_card.nth(i)

            title = card.locator("h2.title").inner_text()

            company = card.locator("h3.company").inner_text()

            location = card.locator("p.location").inner_text()

            posted_date = card.locator("time").get_attribute("datetime")

            link = card.get_by_role("link",name = "Learn").first.get_attribute("href")

            print(f"job {i + 1}")
            print(f"title: {title}")
            print(f"company: {company}")
            print(f"location: {location}")
            print(f"posted date: {posted_date}")
            print(f"link: {link}")
            print("=" * 50)



        browser.close()


# if __name__ == "__main__":
#     main()