"""
Database module for persisting screening results.
Uses SQLite for lightweight data storage.
"""

import sqlite3
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent.parent / "data" / "screener.db"


def init_db(db_path: str = None) -> None:
    """
    Initialize the database schema.
    
    Args:
        db_path: Path to database file
    """
    if db_path is None:
        db_path = str(DB_PATH)
    
    # Ensure data directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create screenings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS screenings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resume_filename TEXT NOT NULL,
            jd_filename TEXT NOT NULL,
            final_score REAL NOT NULL,
            similarity_score REAL,
            skill_match_score REAL,
            rating TEXT,
            feedback TEXT,
            skill_details TEXT,
            resume_text TEXT,
            jd_text TEXT
        )
    """)
    
    # Create candidates table (for bulk/history)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            email TEXT,
            phone TEXT,
            resume_text TEXT,
            resume_filename TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    logger.info(f"Database initialized at {db_path}")


def save_screening_result(result: dict, 
                         resume_filename: str,
                         jd_filename: str,
                         resume_text: str = "",
                         jd_text: str = "",
                         db_path: str = None) -> int:
    """
    Save a screening result to the database.
    
    Args:
        result: Scoring result dict from ResumeMatcher
        resume_filename: Name of the resume file
        jd_filename: Name of the JD file
        resume_text: Original resume text
        jd_text: Original JD text
        db_path: Path to database file
        
    Returns:
        ID of the inserted record
    """
    if db_path is None:
        db_path = str(DB_PATH)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO screenings 
            (resume_filename, jd_filename, final_score, similarity_score, 
             skill_match_score, rating, feedback, skill_details, resume_text, jd_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            resume_filename,
            jd_filename,
            result.get('final_score', 0),
            result.get('similarity_score', 0),
            result.get('skill_match_score', 0),
            result.get('rating', ''),
            result.get('feedback', ''),
            json.dumps(result.get('skill_details', {})),
            resume_text[:5000],  # Limit to 5000 chars for storage
            jd_text[:5000]
        ))
        
        conn.commit()
        screening_id = cursor.lastrowid
        logger.info(f"Saved screening result with ID {screening_id}")
        return screening_id
    
    except Exception as e:
        logger.error(f"Error saving screening result: {e}")
        raise
    finally:
        conn.close()


def get_screening_history(limit: int = 50, db_path: str = None) -> List[Dict]:
    """
    Retrieve screening history.
    
    Args:
        limit: Maximum number of records to retrieve
        db_path: Path to database file
        
    Returns:
        List of screening result dicts
    """
    if db_path is None:
        db_path = str(DB_PATH)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM screenings 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        results = []
        
        for row in rows:
            result = dict(row)
            # Parse skill_details JSON
            if result.get('skill_details'):
                try:
                    result['skill_details'] = json.loads(result['skill_details'])
                except Exception:
                    pass
            results.append(result)
        
        return results
    
    except Exception as e:
        logger.error(f"Error retrieving screening history: {e}")
        return []
    finally:
        conn.close()


def get_screening_by_id(screening_id: int, db_path: str = None) -> Optional[Dict]:
    """
    Retrieve a specific screening result by ID.
    
    Args:
        screening_id: ID of the screening record
        db_path: Path to database file
        
    Returns:
        Screening result dict or None if not found
    """
    if db_path is None:
        db_path = str(DB_PATH)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM screenings WHERE id = ?", (screening_id,))
        row = cursor.fetchone()
        
        if row:
            result = dict(row)
            if result.get('skill_details'):
                try:
                    result['skill_details'] = json.loads(result['skill_details'])
                except Exception:
                    pass
            return result
        return None
    
    except Exception as e:
        logger.error(f"Error retrieving screening {screening_id}: {e}")
        return None
    finally:
        conn.close()


def save_candidate(name: str, email: str, phone: str, 
                  resume_text: str, resume_filename: str,
                  db_path: str = None) -> int:
    """
    Save a candidate's resume information.
    
    Args:
        name: Candidate name
        email: Candidate email
        phone: Candidate phone
        resume_text: Full resume text
        resume_filename: Filename of the resume
        db_path: Path to database file
        
    Returns:
        ID of the inserted candidate record
    """
    if db_path is None:
        db_path = str(DB_PATH)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO candidates 
            (name, email, phone, resume_text, resume_filename)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, resume_text, resume_filename))
        
        conn.commit()
        candidate_id = cursor.lastrowid
        logger.info(f"Saved candidate {name} with ID {candidate_id}")
        return candidate_id
    
    except Exception as e:
        logger.error(f"Error saving candidate: {e}")
        raise
    finally:
        conn.close()


def get_candidates(limit: int = 100, db_path: str = None) -> List[Dict]:
    """
    Retrieve all candidates.
    
    Args:
        limit: Maximum number of records
        db_path: Path to database file
        
    Returns:
        List of candidate dicts
    """
    if db_path is None:
        db_path = str(DB_PATH)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, created_at, name, email, phone, resume_filename 
            FROM candidates 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    except Exception as e:
        logger.error(f"Error retrieving candidates: {e}")
        return []
    finally:
        conn.close()
