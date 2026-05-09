from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.linkedin.com/jobs")

    page.screenshot(path="images/linkedin_jobs.png")

    print("screenshot saved successfully")

    browser.close()

if __name__ == "__main__":
    main()