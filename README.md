# 📄 AI Resume Screener — NLP-Based Resume Matching System

An AI-powered web application that analyses resumes and matches them with job descriptions using Natural Language Processing (NLP) and Machine Learning techniques.

This system helps recruiters and job seekers quickly evaluate resume relevance, identify skill gaps, and improve hiring efficiency.

## 🚀 Features

- 📂 Upload resumes in PDF, DOCX, or TXT format
- 🧠 Automatic text extraction and preprocessing
- 📊 Resume–Job Description similarity scoring using TF-IDF + Cosine Similarity
- ✅ Skill extraction and missing skill detection
- 🌐 User-friendly Flask web interface
- 🧪 Unit-tested components for reliability

## 🧩 Problem Statement

Manual resume screening is time-consuming and error-prone. Recruiters often spend hours reviewing resumes that do not match job requirements.

This project automates the screening process by applying NLP techniques to evaluate resume relevance and provide actionable feedback.

## 🛠️ Tech Stack

| Category        | Tools                            |
| --------------- | -------------------------------- |
| Language        | Python                           |
| ML/NLP          | Scikit-learn, NLTK               |
| Backend         | Flask, Gunicorn                  |
| Parsing         | PyPDF2, python-docx              |
| Frontend        | HTML, CSS, Bootstrap, JavaScript |
| Testing         | Pytest                           |
| Version Control | Git, GitHub                      |
| Deployment      | Render (PaaS)                    |

## 🏗️ System Architecture

User Upload → Text Extraction → Preprocessing → TF-IDF Vectorization → Similarity Calculation → Skill Analysis → Result Display

## 📊 Scoring Methodology

The final resume score is calculated using a weighted combination:

Final Score = 0.5 × Text Similarity + 0.5 × Skill Match Score

Components:

- Text Similarity: Cosine similarity between resume and job description vectors
- Skill Match: Percentage of required skills found in the resume

## 📷 Screenshots (Add Here)

<img width="1920" height="1032" alt="Screenshot 2026-02-06 171824" src="https://github.com/user-attachments/assets/9eca07f6-ddf9-4284-a087-4fb13124fd83" />

<img width="1920" height="1032" alt="Screenshot 2026-02-06 171932" src="https://github.com/user-attachments/assets/4acf73a2-2b44-4619-b81a-605a4b390973" />

<img width="1920" height="1032" alt="Screenshot 2026-02-06 171953" src="https://github.com/user-attachments/assets/b16dfc45-f9e3-4d72-ba3a-8222d397127d" />


## 📦 Installation and Setup

1. Clone the Repository

   ```bash
   git clone https://github.com/Dailydevloper/AI-Resume-Screener.git
   cd AI-Resume-Screener
   ```

2. Create Virtual Environment (Recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. Install Dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Application

   ```bash
   python app.py
   ```

   Open in browser: <http://127.0.0.1:5000>

## 🧪 Running Tests

To run unit tests:

```bash
pytest
```

Tests validate text extraction, scoring logic, and API responses.

## 📈 Example Output

Resume Match Score: 78%

Matched Skills:

- Python
- Machine Learning
- Pandas

Missing Skills:

- Docker
- Cloud Deployment
- SQL

Recommendation: Add deployment and database projects to improve the profile.

## 📂 Project Structure

```text
AI-Resume-Screener/
├── app.py
├── README.md
├── render.yaml
├── templates/
│   ├── base.html
│   ├── history.html
│   └── index.html
├── static/
│   ├── main.js
│   └── styles.css
├── screener/
│   ├── __init__.py
│   ├── db.py
│   ├── nlp.py
│   ├── parsing.py
│   └── scoring.py
├── uploads/
│   ├── 20260205_223727_test_resume.txt
│   └── 20260205_224738_Profile.pdf
├── requirements.txt
├── test_app.py
├── test_jd.txt
└── test_resume.txt
```


### Live Demo

Demo: https://ai-resume-screener-atif.onrender.com

## ⚠️ Limitations

- Does not use deep contextual embeddings (e.g., BERT)
- Performance depends on resume formatting
- Limited to predefined skill sets
- No multilingual support currently

## 🔮 Future Enhancements

- Integration of BERT / Transformer models
- Skill weighting based on job role
- Resume ranking dashboard
- User authentication system
- Cloud-based storage

## 👨‍💻 Author

Prateek Dwivedi

B.Tech Student | AI and Machine Learning Enthusiast

GitHub: <https://github.com/Dailydevloper>

## 📜 License

This project is licensed under the MIT License.
