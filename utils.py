import re
import io
import PyPDF2
from skills import skills_list
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def extract_text_from_pdf(file_bytes):
    text = ""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text.strip()

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_skills(text):
    text = clean_text(text)
    found_skills = []
    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)
    return sorted(list(set(found_skills)))

def calculate_skill_match(resume_skills, jd_skills):
    resume_set = set([s.lower() for s in resume_skills])
    jd_set = set([s.lower() for s in jd_skills])

    matched = sorted(list(resume_set.intersection(jd_set)))
    missing = sorted(list(jd_set - resume_set))
    score = round((len(matched) / len(jd_set)) * 100, 2) if jd_set else 0

    return score, matched, missing

def calculate_cosine_similarity(resume_text, jd_text):
    docs = [resume_text, jd_text]
    tfidf = TfidfVectorizer()
    matrix = tfidf.fit_transform(docs)
    similarity = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(similarity * 100, 2)

def top_recommended_roles(resume_skills):
    role_keywords = {
        "Data Analyst": ["sql", "excel", "power bi", "tableau", "pandas", "statistics"],
        "ML Intern": ["python", "machine learning", "scikit-learn", "tensorflow", "keras", "numpy"],
        "NLP Intern": ["nlp", "nltk", "spacy", "transformers", "huggingface"],
        "Web Developer": ["html", "css", "javascript", "react", "mongodb"],
        "Python Developer": ["python", "fastapi", "flask", "sql", "git"]
    }

    scores = []
    resume_set = set([s.lower() for s in resume_skills])

    for role, keywords in role_keywords.items():
        match_count = len(resume_set.intersection(set(keywords)))
        scores.append({"role": role, "score": match_count})

    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:3]

def generate_pdf_report(data):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "AI Resume Analyzer Report")
    y -= 30

    pdf.setFont("Helvetica", 10)

    for idx, result in enumerate(data.get("results", []), start=1):
        lines = [
            f"Resume #{idx}: {result.get('file_name', '')}",
            f"Predicted Role: {result.get('predicted_role', '')}",
            f"Skill Match Score: {result.get('skill_score', 0)}%",
            f"Text Similarity Score: {result.get('similarity_score', 0)}%",
            f"ATS Score: {result.get('ats_score', 0)}%",
            f"Matched Skills: {', '.join(result.get('matched_skills', []))}",
            f"Missing Skills: {', '.join(result.get('missing_skills', []))}",
            f"Recommended Roles: {', '.join([r['role'] for r in result.get('recommended_roles', [])])}",
            "-" * 90
        ]

        for line in lines:
            pdf.drawString(50, y, line[:110])
            y -= 18
            if y < 80:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - 50

    pdf.save()
    buffer.seek(0)
    return buffer