from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz

app = FastAPI(title="SmartHire AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text(content: bytes, filename: str) -> str:
    if filename.endswith(".pdf"):
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    return content.decode("utf-8", errors="ignore")

def calculate_score(resume_text: str, required_skills: list):
    resume_lower = resume_text.lower()
    found = []
    missing = []
    for skill in required_skills:
        if skill.strip().lower() in resume_lower:
            found.append(skill.strip())
        else:
            missing.append(skill.strip())
    if len(required_skills) == 0:
        return 0, [], []
    score = round((len(found) / len(required_skills)) * 100)
    return score, found, missing

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
    required_skills: str = "python,fastapi,react,html,css,javascript,java,sql,spring,aws,kubernetes"
):
    content = await resume.read()
    resume_text = extract_text(content, resume.filename)
    skills_list = [s.strip() for s in required_skills.split(",")]
    score, found, missing = calculate_score(resume_text, skills_list)
    return {
        "filename": resume.filename,
        "score": score,
        "found_skills": found,
        "missing_skills": missing,
        "recommendation": "Strong candidate" if score >= 70 else "Needs review" if score >= 40 else "Not recommended"
    }