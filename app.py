"""
Flask application for AI-Powered Resume Screener
Main entry point for the web application.
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, jsonify
from screener.parsing import extract_text_from_file, clean_text, extract_contact_info
from screener.nlp import SkillExtractor, preprocess_text
from screener.scoring import ResumeMatcher
from screener.db import init_db, save_screening_result, get_screening_history, get_screening_by_id, save_candidate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}

# Create upload folder if it doesn't exist
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)

# Initialize database
init_db()

# Initialize components
skill_extractor = SkillExtractor()
matcher = ResumeMatcher()


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def save_uploaded_file(file) -> str:
    """Save uploaded file and return path."""
    if not file or file.filename == '':
        raise ValueError("No file selected")
    
    if not allowed_file(file.filename):
        raise ValueError(f"File type not allowed. Allowed: {', '.join(app.config['ALLOWED_EXTENSIONS'])}")
    
    filename = secure_filename(file.filename)
    # Add timestamp to avoid conflicts
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    logger.info(f"File saved: {filepath}")
    return filepath


@app.route('/')
def index():
    """Home page - upload resume and JD."""
    return render_template('index.html')


@app.route('/api/screen', methods=['POST'])
def screen_resume():
    """
    API endpoint to screen a resume against a job description.
    Expects multipart form with 'resume' and 'jd_text' fields.
    """
    try:
        # Check for resume file
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        resume_file = request.files['resume']
        jd_text = request.form.get('jd_text', '').strip()
        
        if not jd_text:
            return jsonify({'error': 'No job description provided'}), 400
        
        # Save and extract resume
        resume_path = save_uploaded_file(resume_file)
        resume_text = extract_text_from_file(resume_path)
        
        # Clean texts
        resume_clean = clean_text(resume_text)
        jd_clean = clean_text(jd_text)
        
        # Preprocess for NLP
        resume_processed = preprocess_text(resume_clean)
        jd_processed = preprocess_text(jd_clean)
        
        # Extract skills
        resume_skills = skill_extractor.extract_skills(resume_processed)
        jd_skills = skill_extractor.extract_skills(jd_processed)
        
        # Score resume
        result = matcher.score_resume(
            resume_processed, 
            jd_processed, 
            resume_skills, 
            jd_skills
        )
        
        # Extract candidate info
        candidate_info = extract_contact_info(resume_text)
        
        # Save to database
        screening_id = save_screening_result(
            result,
            resume_file.filename,
            'uploaded_jd.txt',
            resume_text,
            jd_text
        )
        
        # Save candidate if we have a name
        if candidate_info.get('name'):
            save_candidate(
                candidate_info['name'],
                candidate_info.get('email', ''),
                candidate_info.get('phone', ''),
                resume_text,
                resume_file.filename
            )
        
        # Return result with candidate info
        result['screening_id'] = screening_id
        result['candidate_info'] = candidate_info
        result['resume_skills'] = resume_skills
        result['jd_skills'] = jd_skills
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error screening resume: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/results')
def results():
    """Results page."""
    return render_template('results.html')


@app.route('/history')
def history():
    """History page - view past screenings."""
    return render_template('history.html')


@app.route('/api/history', methods=['GET'])
def get_history():
    """API endpoint to get screening history."""
    try:
        limit = request.args.get('limit', 50, type=int)
        history_data = get_screening_history(limit)
        return jsonify(history_data), 200
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/screening/<int:screening_id>', methods=['GET'])
def get_screening(screening_id):
    """API endpoint to get a specific screening by ID."""
    try:
        screening = get_screening_by_id(screening_id)
        if not screening:
            return jsonify({'error': 'Screening not found'}), 404
        return jsonify(screening), 200
    except Exception as e:
        logger.error(f"Error retrieving screening: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'}), 200


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({'error': 'File size exceeds 50MB limit'}), 413


@app.errorhandler(500)
def internal_error(error):
    """Handle internal errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Run in debug mode (set to False in production)
    app.run(debug=True, host='0.0.0.0', port=5000)
