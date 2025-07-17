# parser.py

import re
import spacy

nlp = spacy.load('en_core_web_sm')

skills_list = [
    'python', 'java', 'c++', 'sql', 'excel', 'power bi',
    'machine learning', 'deep learning', 'django', 'flask',
    'communication', 'teamwork', 'git', 'github', 'data analysis'
]

def extract_name(text):
    """Extracts the first PERSON named entity."""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return None

def extract_email(text):
    """Finds the first email address in the text."""
    match = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.\w+", text)
    return match[0] if match else None

def extract_phone(text):
    """Finds the first phone number in the text."""
    match = re.findall(r'\+?\d[\d\s\-]{8,15}', text)
    return match[0] if match else None

def extract_skills(text):
    """Returns a list of skills present in the text."""
    text = text.lower()
    found_skills = [skill for skill in skills_list if skill in text]
    return list(set(found_skills))
def extract_job_title(text):
    """
    Attempts to extract the job title by looking for patterns like:
    'Objective: Seeking a role as a Data Scientist', or first few lines.
    """
    job_keywords = [
        'software engineer', 'data scientist', 'web developer', 'data analyst',
        'machine learning engineer', 'project manager', 'frontend developer',
        'backend developer', 'full stack developer', 'AI engineer'
    ]

    text_lower = text.lower()
    for job in job_keywords:
        if job in text_lower:
            return job.title()

    # fallback: try first 5 lines
    lines = text.split('\n')
    for line in lines[:5]:
        for job in job_keywords:
            if job in line.lower():
                return job.title()

    return "Not Found"

