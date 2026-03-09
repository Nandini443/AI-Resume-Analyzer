from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import io

from utils import (
    extract_text_from_pdf,
    clean_text,
    extract_skills,
    calculate_skill_match,
    calculate_cosine_similarity,
    top_recommended_roles,
    generate_pdf_report
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

role_model = joblib.load("model/role_model.pkl")

JD_TEMPLATES = {
    "ml_intern": """We are looking for a Machine Learning Intern with knowledge of Python, NumPy, Pandas, Scikit-learn, TensorFlow, SQL, NLP, and model evaluation.""",
    "data_analyst": """We are looking for a Data Analyst Intern with knowledge of Excel, SQL, Python, Pandas, Power BI, Tableau, and data visualization.""",
    "nlp_intern": """We are looking for an NLP Intern with knowledge of Python, NLTK, spaCy, Transformers, HuggingFace, text classification, and preprocessing.""",
    "python_dev": """We are looking for a Python Developer Intern with Python, FastAPI, Flask, SQL, APIs, Git, and backend development skills."""
}

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/jd-template/{template_name}")
async def get_jd_template(template_name: str):
    template = JD_TEMPLATES.get(template_name, "")
    return JSONResponse({"template": template})

@app.post("/analyze")
async def analyze_resume(
    resumes: list[UploadFile] = File(...),
    job_description: str = Form(...)
):
    jd_clean = clean_text(job_description)
    jd_skills = extract_skills(jd_clean)

    results = []

    for resume in resumes:
        file_bytes = await resume.read()
        resume_text = extract_text_from_pdf(file_bytes)
        cleaned_resume = clean_text(resume_text)
        resume_skills = extract_skills(cleaned_resume)

        skill_score, matched_skills, missing_skills = calculate_skill_match(resume_skills, jd_skills)
        similarity_score = calculate_cosine_similarity(cleaned_resume, jd_clean)
        ats_score = round((skill_score * 0.6) + (similarity_score * 0.4), 2)

        predicted_role = role_model.predict([cleaned_resume])[0]
        recommended_roles = top_recommended_roles(resume_skills)

        results.append({
            "file_name": resume.filename,
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "skill_score": skill_score,
            "similarity_score": similarity_score,
            "ats_score": ats_score,
            "predicted_role": predicted_role,
            "recommended_roles": recommended_roles,
            "resume_text": resume_text[:2000]
        })

    return JSONResponse({"results": results})

@app.post("/download-pdf")
async def download_pdf(request: Request):
    data = await request.json()
    pdf_buffer = generate_pdf_report(data)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=resume_analysis_report.pdf"}
    )