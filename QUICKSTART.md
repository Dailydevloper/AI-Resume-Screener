# Quick Start Guide

## Local Development

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd AI-Resume-Screener
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   python app.py
   ```

5. **Access the application:**
   Open your browser and go to `http://localhost:5000`

## Project Structure

```text
AI-Resume-Screener/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── render.yaml            # Render deployment config
├── Procfile               # Alternative deployment config
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── DEPLOYMENT.md          # Detailed deployment guide
├── data/
│   └── skills.json        # Skills taxonomy database
├── screener/
│   ├── __init__.py
│   ├── db.py             # Database operations
│   ├── nlp.py            # NLP and skill extraction
│   ├── parsing.py        # Resume/JD text extraction
│   └── scoring.py        # Similarity and scoring logic
├── static/
│   ├── main.js           # Frontend JavaScript
│   └── styles.css        # Custom styles
├── templates/
│   ├── base.html         # Base template
│   ├── history.html      # Screening history page
│   └── index.html        # Main upload page
├── uploads/              # Uploaded resume files (gitignored)
└── test_app.py          # Application tests
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Development
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Production (set in Render dashboard)
FLASK_ENV=production
SECRET_KEY=<generate-strong-key>
DATABASE_PATH=/opt/render/project/src/data/screener.db
```

## Running Tests

```bash
pytest
```

## API Endpoints

### POST /api/screen

Screen a resume against a job description.

**Request:**

- `resume`: File upload (PDF, DOCX, or TXT)
- `jd_text`: Job description text

**Response:**

```json
{
  "final_score": 0.78,
  "similarity_score": 0.75,
  "skill_match_score": 0.81,
  "rating": "Good Match",
  "feedback": "Strong candidate...",
  "screening_id": 123,
  "candidate_info": {...},
  "resume_skills": {...},
  "jd_skills": {...}
}
```

### GET /api/history

Get screening history.

**Query Parameters:**

- `limit`: Number of records (default: 50)

### GET /api/screening/:id

Get a specific screening by ID.

### GET /api/health

Health check endpoint.

## Development Tips

1. **Database Location:**
   - Development: `data/screener.db`
   - Production: Set via `DATABASE_PATH` environment variable

2. **File Uploads:**
   - Max size: 50MB
   - Allowed formats: PDF, DOCX, TXT
   - Stored in: `uploads/` directory

3. **NLTK Data:**
   - Required: `punkt`, `stopwords`, `punkt_tab`
   - Auto-downloaded on first run

4. **Logs:**
   - Check console output for debugging
   - Production logs: Render dashboard

## Troubleshooting

### NLTK Download Error

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Database Not Initializing

```bash
# Manually initialize
python -c "from screener.db import init_db; init_db()"
```

### Port Already in Use

```bash
# Change port
export PORT=8000  # Linux/macOS
set PORT=8000     # Windows

python app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details
