import pandas as pd
from datetime import datetime
from pathlib import Path

def export_jobs_to_excel(jobs, output_path = "output/jobs.xlsx"):

    # export jobs to excel file

    #  add timestamp to job
    for job in jobs:
        job["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # create data frame
    df = pd.DataFrame(jobs)


    # create output path  if not exist 
    Path("output").mkdir(exist_ok=True) 


    # export to excel
    df.to_excel(output_path, index=False)


    print(f"Saved {len(jobs)} to {output_path}")

