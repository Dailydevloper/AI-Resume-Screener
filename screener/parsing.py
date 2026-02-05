"""
Resume and Job Description text extraction module.
Supports PDF, DOCX, and plain text formats.
"""

import re
import PyPDF2
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
        
    Raises:
        ValueError: If PDF is empty or corrupted
    """
    try:
        text = []
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            if len(reader.pages) == 0:
                raise ValueError("PDF file is empty.")
            
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
                except Exception as e:
                    logger.warning(f"Could not extract text from page {page_num}: {e}")
        
        if not text:
            raise ValueError("No text could be extracted from the PDF.")
        
        return "\n".join(text)
    
    except Exception as e:
        logger.error(f"Error processing PDF {file_path}: {e}")
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file.
    
    Args:
        file_path: Path to the DOCX file
        
    Returns:
        Extracted text as a string
    """
    try:
        from docx import Document
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        if not text.strip():
            raise ValueError("DOCX file is empty or contains no text.")
        return text
    except Exception as e:
        logger.error(f"Error processing DOCX {file_path}: {e}")
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")


def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from a file (PDF, DOCX, or TXT).
    Auto-detects format based on file extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Extracted text
        
    Raises:
        ValueError: If file format is unsupported or extraction fails
    """
    path = Path(file_path)
    
    if not path.exists():
        raise ValueError(f"File not found: {file_path}")
    
    suffix = path.suffix.lower()
    
    if suffix == '.pdf':
        return extract_text_from_pdf(file_path)
    elif suffix == '.docx':
        return extract_text_from_docx(file_path)
    elif suffix == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
            if not text:
                raise ValueError("Text file is empty.")
            return text
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def clean_text(text: str) -> str:
    """
    Clean and normalize text for NLP processing.
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    # Remove special characters but keep alphanumeric, spaces, and common punctuation
    text = re.sub(r'[^\w\s\-\.]', ' ', text)
    return text


def extract_contact_info(text: str) -> dict:
    """
    Extract basic contact information from resume text.
    
    Args:
        text: Resume text
        
    Returns:
        Dictionary with email, phone, and name candidates
    """
    info = {
        'email': None,
        'phone': None,
        'name': None
    }
    
    # Extract email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_match = re.search(email_pattern, text)
    if email_match:
        info['email'] = email_match.group()
    
    # Extract phone (basic US format)
    phone_pattern = r'(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        info['phone'] = phone_match.group()
    
    # Extract name (first line that looks like a name)
    lines = text.split('\n')
    for line in lines[:5]:  # Check first 5 lines
        cleaned = line.strip()
        if cleaned and 2 <= len(cleaned.split()) <= 4 and len(cleaned) < 60:
            info['name'] = cleaned
            break
    
    return info
