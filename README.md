# AI Resume Analyzer

AI Resume Analyzer is a full-stack web application that analyzes resumes using Natural Language Processing (NLP) and Machine Learning.  
It compares resumes with job descriptions, predicts suitable job roles, identifies skill gaps, and generates visual insights with downloadable reports.

---

## 🚀 Features

- Resume PDF parsing
- NLP-based skill extraction
- Resume vs Job Description matching
- Skill match score calculation
- Cosine similarity text comparison
- Machine Learning role prediction
- Recommended job roles
- Interactive charts and skill visualization
- Drag-and-drop resume upload
- Multiple resume comparison
- Job Description templates
- Login page interface
- Downloadable PDF analysis report

---

## 🧠 Machine Learning Techniques

- TF-IDF Vectorization
- Cosine Similarity
- Logistic Regression for role prediction
- NLP text preprocessing

---

## 🛠 Tech Stack

### Backend
- Python
- FastAPI
- Scikit-learn
- PyPDF2
- ReportLab

### Frontend
- HTML
- CSS
- JavaScript
- Chart.js

### Tools
- Git
- GitHub
- VS Code

---
AI_Resume_Analyzer
│
├── main.py
├── utils.py
├── skills.py
├── train_model.py
├── requirements.txt
├── README.md
│
├── model/
│ └── role_model.pkl
│
├── templates/
│ ├── login.html
│ └── index.html
│
└── static/
├── style.css
└── script.js


---

## ⚙ Installation

Clone the repository


git clone https://github.com/YOUR_USERNAME/AI-Resume-Analyzer.git


Navigate to project folder


cd AI-Resume-Analyzer


Install dependencies


pip install -r requirements.txt


Train ML model


python train_model.py


Run the application


uvicorn main:app --reload


Open in browser


http://127.0.0.1:8000


---

## 📊 Example Workflow

1. Upload one or multiple resume PDFs
2. Paste or choose a job description template
3. Analyze resumes
4. View skill match scores
5. See missing skills and recommendations
6. View predicted role
7. Compare multiple candidates
8. Download analysis report

---

## 📈 Future Improvements

- Semantic resume matching using BERT embeddings
- Resume ranking system for recruiters
- Skill gap learning roadmap
- AI-based resume improvement suggestions
- Career recommendation engine
- Admin dashboard for recruiters

---

## 👩‍💻 Author

**Nandinipapisetti**

Computer Science (Data Science) Student  
Interested in AI, Machine Learning, NLP and Data Analytics.

