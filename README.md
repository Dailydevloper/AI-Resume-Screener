# 🤖 AI-Powered Resume Screener (ATS Lite)

An intelligent resume screening system that analyzes resumes against job descriptions using Natural Language Processing (NLP) and machine learning. Perfect for HR professionals, recruiters, and tech teams looking for an automated, beginner-friendly ATS solution.

## ✨ Features

✅ **PDF/DOCX/TXT Support** - Extract text from multiple document formats  
✅ **Intelligent Skill Matching** - Identify technical and soft skills automatically  
✅ **TF-IDF Scoring** - Advanced text similarity analysis  
✅ **Candidate Profiling** - Extract name, email, and phone from resumes  
✅ **Detailed Feedback** - Get actionable insights on each screening  
✅ **Screening History** - Persistent storage of all screenings  
✅ **Bootstrap UI** - Clean, responsive, mobile-friendly interface  
✅ **Industry-Ready** - Mimics real ATS systems used by Fortune 500 companies

## 🛠️ Tech Stack

- **Backend:** Flask, Python 3.14+
- **NLP:** NLTK, SpaCy
- **ML:** Scikit-learn (TF-IDF), NumPy, Pandas
- **File Processing:** PyPDF2, pdfplumber, python-docx
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Data Viz:** Matplotlib, Seaborn, Chart.js
- **Deployment:** Render, Gunicorn

## 📋 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Dailydevloper/AI-Resume-Screener.git
   cd AI-Resume-Screener
   ```

2. **Create a virtual environment:**

   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data (first time only):**

   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

5. **Run the application:**

   ```bash
   python app.py
   ```

   The app will start at: **<http://localhost:5000>**

## 🚀 Usage

1. **Open the home page** (<http://localhost:5000>)
2. **Upload a resume** (PDF, DOCX, or TXT)
3. **Paste a job description** in the text area
4. **Click "Screen Resume"** to analyze
5. **View results** including:
   - Overall match score (0-100)
   - Similarity percentage
   - Skill match coverage
   - Matched/missing skills
   - Personalized feedback
6. **Check history** to review past screenings

## 📊 How Scoring Works

### Final Score = (Similarity × 0.5) + (Skill Match × 0.5)

- **Similarity Score (50%):** TF-IDF cosine similarity between resume and job description
- **Skill Match Score (50%):** Ratio of matched skills to required skills
- **Final Score Range:** 0-100

### Rating Scale

- ⭐⭐⭐⭐⭐ (80-100): Excellent match
- ⭐⭐⭐⭐ (60-79): Good match
- ⭐⭐⭐ (40-59): Partial match
- ⭐⭐ (20-39): Limited match
- ⭐ (0-19): Poor match

## 📁 Project Structure

```text
AI-Resume-Screener/
├── app.py                      # Flask entry point
├── requirements.txt            # Python dependencies
├── screener/
│   ├── __init__.py
│   ├── parsing.py             # PDF/DOCX extraction
│   ├── nlp.py                 # NLP & skill extraction
│   ├── scoring.py             # Scoring & matching
│   └── db.py                  # Database operations
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Upload page
│   ├── results.html           # Results page
│   └── history.html           # History page
├── static/
│   ├── styles.css             # Custom styling
│   └── main.js                # Frontend scripts
├── data/
│   ├── skills.json            # Skills taxonomy
│   └── screener.db            # SQLite database (auto-created)
├── uploads/                   # Uploaded resume files
└── README.md                  # This file
```

## 🧠 Skills Taxonomy

The system includes a comprehensive skills taxonomy covering:

- **Programming Languages:** Python, Java, JavaScript, C++, Go, Rust, etc.
- **Web Frameworks:** Django, Flask, FastAPI, React, Angular, Vue, etc.
- **Databases:** SQL, MySQL, PostgreSQL, MongoDB, Redis, Cassandra, etc.
- **Cloud Platforms:** AWS, Azure, GCP, Kubernetes, Docker, etc.
- **Data Science:** Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch, R, Spark, etc.
- **DevOps Tools:** Git, GitHub, Jenkins, CI/CD, Terraform, Ansible, etc.
- **Soft Skills:** Agile, Scrum, Leadership, Communication, Project Management, etc.

Customize `data/skills.json` to add more skills or adjust categories.

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in the root directory:

```env
FLASK_ENV=production
DEBUG=False
MAX_UPLOADS=50
```

### Database

The SQLite database is automatically created in `data/screener.db` on first run.

**Schema:**

- `screenings` - Stores screening results
- `candidates` - Stores candidate information

## 🧪 Testing

### Manual Testing (Recommended MVP approach)

1. **Test with sample resume:**
   - Create a simple text resume with common skills
   - Upload a PDF version
   - Compare extraction accuracy

2. **Test edge cases:**
   - Empty PDF
   - Very long resume (10+ pages)
   - Multi-format file uploads

3. **Verify scoring:**
   - Perfect match: resume text = job description
   - Partial match: 60-70% skill overlap
   - Poor match: completely different skills

### Sample Data

Example resume text:

```text
John Doe
john.doe@email.com
(555) 123-4567

Senior Python Developer with 5+ years experience
- Strong experience with Django and FastAPI
- MongoDB and PostgreSQL databases
- AWS and Docker deployment
- Git version control
```

Example job description:

```text
Seeking Senior Backend Engineer
Required Skills:
- Python programming
- Django or Flask framework
- Relational database (SQL, PostgreSQL)
- AWS or cloud experience
- Docker containerization
- RESTful API design
```

Expected: **High match score (~85)**

## 📊 Data Visualization (Future Enhancement)

The app is set up for Chart.js integration. Future versions will include:

- Score distribution charts
- Skill match heatmaps
- Candidate comparison graphs
- Trending common skills

## 🚀 Deployment

### Deploy to Render

1. **Push to GitHub:**

   ```bash
   git push origin main
   ```

2. **Connect to Render:**
   - Go to <https://render.com>
   - Create new Web Service
   - Connect GitHub repository
   - Use `gunicorn app:app` as start command
   - Set environment to Python 3.14

3. **The app will auto-deploy on every push to main**

### Deploy to Heroku

```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Deploy to AWS/GCP

See individual provider documentation or use their CLI tools.

## 🤝 Contributing

Contributions welcome! Ideas:

- Add more NLP models (Word2Vec, BERT)
- Implement batch resume screening
- Add resume parsing for specific fields
- Create admin dashboard
- Add API authentication
- Multi-language support

## 📝 License

MIT License - Feel free to use, modify, and distribute.

## 👨‍💻 Author

**Dailydevloper** - Building AI-powered HR solutions

## 📧 Support

- Report bugs on GitHub Issues
- Suggest features via Discussions
- Star ⭐ if you found this helpful!

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [NLTK Book](https://www.nltk.org/book/)
- [Scikit-learn Guide](https://scikit-learn.org/stable/)
- [Natural Language Processing with SpaCy](https://spacy.io/)

## 🎯 Roadmap

- [ ] Advanced NLP models (BERT, RoBERTa)
- [ ] Batch resume screening
- [ ] Resume comparison/ranking
- [ ] Admin analytics dashboard
- [ ] API for third-party integrations
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Resume parsing templates

---

## Build smarter hiring workflows with AI! 🚀
