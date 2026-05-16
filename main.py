from playwright.sync_api import sync_playwright
from scraper.job_scraper import scrape_jobs
from exporter.excel_exporter import export_jobs_to_excel
from pathlib import Path
from analyzer.llm_analyzer import analyze_jobs
import json
import pandas as pd


DATA_PATH = Path("data/fake_jobs.json")
OUTPUT_JSON = Path("output/job_analysis.json")
OUTPUT_EXCEL = Path("output/job_analysis.xlsx")

def load_jobs():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
    

def save_analysis(results):
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    df = pd.DataFrame(results)

    for col in df.columns:
        df[col] = df[col].apply(
            lambda value: ", ".join(value) if isinstance(value, list) else value
        )

    df.to_excel(OUTPUT_EXCEL, index=False)

    print(f"Saved JSON to: {OUTPUT_JSON}")
    print(f"Saved Excel to: {OUTPUT_EXCEL}")



def main():

    jobs = load_jobs()
    results = analyze_jobs(jobs)
    save_analysis(results)


    # keywords = input("Enter a keyword to search for: ").lower()
    # if "," in keywords:
    #     keywords = [k.strip() for k in keywords.split(",")]
    # else:
    #     keywords = [keywords.strip()]
    # jobs = scrape_jobs(keywords)

    # export_jobs_to_excel(jobs)



    # print("\nResults")
    # print("=" * 50)
    # for(job) in jobs:
    #     print("Title:", job["title"])
    #     print("Company:", job["company"])
    #     print("Location:", job["location"])
    #     print("Description:", job["description"])
    #     print("posted at:", job["posted"])
    #     print("=" * 50)


    

if __name__ == "__main__":
    main()