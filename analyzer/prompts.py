SYSTEM_PROMPT = """
You are a job description analyzer.

Your task is to analyze a job description and return structured JSON.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations.
Do not wrap the JSON in ```.

JSON format:
{
  "required_skills": [],
  "preferred_skills": [],
  "technologies": [],
  "seniority_level": "",
  "responsibilities": [],
  "important_keywords": [],
  "missing_skills": [],
  "resume_suggestions": "",
  "summary": ""
}
"""


def build_job_analysis_prompt(job):
    return f"""
{SYSTEM_PROMPT}

Job Title:
{job.get("title", "")}

Company:
{job.get("company", "")}

Location:
{job.get("location", "")}

Job Description:
{job.get("description", "")}
"""