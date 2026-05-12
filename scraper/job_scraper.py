from playwright.sync_api import sync_playwright
import time

def scrape_jobs():
    jobs = []
    baseUrl = "https://realpython.github.io/fake-jobs/"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(baseUrl)

        page.wait_for_timeout(3000)

        # locate job content
        job_card = page.locator(".card-content")
        
        count = job_card.count()

        print(f"{count} jobs found\n")

        # iterate through first 5  jobs and extract job information 
        # page.pause()
        print("=" * 50)
        for i in range(min(count,5)):
            try:
                card = job_card.nth(i)

                title = card.locator("h2.title").inner_text()

                apply_link = card.get_by_role("link",name = "Apply").first.get_attribute("href")

                print(f"Opening :{title}")

                #  create new page
                detail_page =browser.new_page()
                
                # go to job detail page
                detail_page.goto(apply_link)

                detail_page.wait_for_timeout(2000)

                job_container = detail_page.locator("#ResultsContainer")

                job_title = job_container.locator("h1.title").inner_text()

                job_company = job_container.locator("h2.company").inner_text()

                job_content = job_container.locator("div.content")
                
                job_description = job_content.locator("p:not(#location):not(#date)").inner_text()

                job_location = job_content.locator("#location").inner_text().replace("Location","").strip()

                job_posted = job_content.locator("#date").inner_text().replace("Posted","").strip()

                #  save job to list
                job_data = {
                    "title": job_title,
                    "company": job_company,
                    "location": job_location,
                    "description": job_description,
                    "posted": job_posted,
                    "link": apply_link
                }

                jobs.append(job_data)
               
            except Exception as e:
                print(f"Error scraping job {i}: {e}")


            # print("=" * 50)
            # print(f"Job Title: {job_title}")
            # print(f"Job Company: {job_company}")
            # print(f"Job Location: {job_location}")
            # print(f"Job Description: {job_description}")
            # print("=" * 50)

            detail_page.close()
            time.sleep(1)
        browser.close()

    return jobs


# if __name__ == "__main__":
#     scrape_jobs()