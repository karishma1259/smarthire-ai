from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI(title="SmartHire AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobDescription(BaseModel):
    title: str
    description: str
    required_skills: list[str]

def extract_skills(text: str, skills: list[str]):
    text_lower = text.lower()
    found = []
    for skill in skills:
        if skill.lower() in text_lower:
            found.append(skill)
    return found

def calculate_score(resume_text: str, required_skills: list[str]):
    found_skills = extract_skills(resume_text, required_skills)
    score = (len(found_skills) / len(required_skills)) * 100
    return round(score), found_skills

@app.get("/")
def home():
    return {"message": "SmartHire AI is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/screen")
async def screen_resume(
    resume: UploadFile = File(...),
    job_title: str = "Software Engineer",
    required_skills: str = "python,fastapi,react"
):
    content = await resume.read()
    resume_text = content.decode("utf-8", errors="ignore")
    skills_list = [s.strip() for s in required_skills.split(",")]
    score, found_skills = calculate_score(resume_text, skills_list)
    missing_skills = [s for s in skills_list if s not in found_skills]
    return {
        "filename": resume.filename,
        "score": score,
        "found_skills": found_skills,
        "missing_skills": missing_skills,
        "recommendation": "Strong candidate" if score >= 70 else "Needs review" if score >= 40 else "Not recommended"
    }