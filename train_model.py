import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

data = {
    "resume_text": [
        "python sql pandas excel power bi statistics data analysis tableau",
        "python tensorflow keras deep learning machine learning numpy scikit-learn",
        "html css javascript react node mongodb frontend web",
        "python fastapi flask api backend sql git github",
        "nlp nltk spacy transformers huggingface text classification"
    ],
    "role": [
        "Data Analyst",
        "ML Intern",
        "Web Developer",
        "Python Developer",
        "NLP Intern"
    ]
}

df = pd.DataFrame(data)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=1000))
])

pipeline.fit(df["resume_text"], df["role"])

joblib.dump(pipeline, "model/role_model.pkl")
print("Model saved successfully.")