import json
import requests
from analyzer.prompts import build_job_analysis_prompt


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:14b"


def analyze_job(job):
    prompt = build_job_analysis_prompt(job)

    playload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    response = requests.post(OLLAMA_URL, json=playload, timeout = 120)
    response.raise_for_status()

    raw_text = response.json().get("response", "")

    try:
        analysis = json.loads(raw_text)

    except json.JSONDecodeError:
        analysis = {
            "required_skills": [],
            "preferred_skills": [],
            "technologies": [],
            "seniority_level": "",
            "responsibilities": [],
            "important_keywords": [],
            "missing_skills": [],
            "resume_suggestions": "",
            "summary": "",
            "raw_response": raw_text
        }
    
    return {
        "title": job.get("title", ""),
        "company": job.get("company", ""),
        "location": job.get("location", ""),
        "url": job.get("url", ""),
        **analysis
    }



def analyze_jobs(jobs, limit = 3):
    results = []
    for job in jobs[:limit]:
        print(f"Analyzing: {job.get('title', '')}")
        result = analyze_job(job)
        results.append(result)
        print("=" * 50)
        print(result)

    return results