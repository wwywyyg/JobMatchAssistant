from playwright.sync_api import sync_playwright
import time

def scrape_jobs(keywords):
    jobs = []
    baseUrl = "https://realpython.github.io/fake-jobs/"
    repeat_url = set()
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

                # handle empty strings 
                job_title = job_title.strip() if job_title else "N/A"
                job_company = job_company.strip() if job_company else "N/A"
                job_location = job_location.strip() if job_location else "N/A"
                job_description = job_description.strip() if job_description else "N/A"
                job_posted = job_posted.strip() if job_posted else "N/A"

                #  save job to list
                job_data = {
                    "title": job_title,
                    "company": job_company,
                    "location": job_location,
                    "description": job_description,
                    "posted": job_posted,
                    "url": apply_link
                }
                
                # cheak if job matches keyword
                if is_matching_job(job_data,keywords):

                    # check if job url already exists
                    url = job_data.get("url")
                    if url in repeat_url:
                        continue
                    repeat_url.add(url)
                    # add job to list
                    jobs.append(job_data)

            except Exception as e:
                print(f"Error scraping job {i}: {e}")
                with open("logs/failed_urls.txt","a") as file:
                    file.write(f"{apply_link}\n")
            finally:
                if detail_page:
                    detail_page.close()
            
            time.sleep(1)
        browser.close()
        print(f"total match jobs collected : {len(jobs)}")
        print(f"unique jobs found : {len(repeat_url)}")

        # print out job info
        for job in jobs:
            print("=" * 50)
            print(f"Title: {job.get('title')}")
            print(f"Company: {job.get('company')}")
            print(f"Location: {job.get('location')}")
            print(f"Description: {job.get('description')}")
            print(f"Posted: {job.get('posted')}")
            print(f"url: {url}")


    return jobs

# helper

def is_matching_job(job,keywords):
    if not keywords:
        return True
    title = job.get("title","").lower()
    description = job.get("description","").lower()

    for keyword in keywords:
        keyword = keyword.lower()
        if keyword in title or keyword in description:
            return True
    return False


# if __name__ == "__main__":
#     scrape_jobs()