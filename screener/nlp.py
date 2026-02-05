"""
Natural Language Processing module for resume analysis.
Handles text preprocessing, tokenization, and skill extraction.
"""

import re
import json
import logging
from typing import List, Dict
from pathlib import Path
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class SkillExtractor:
    """Extract skills from text using keyword matching and NLP."""
    
    def __init__(self, skills_file: str = None):
        """
        Initialize the skill extractor.
        
        Args:
            skills_file: Path to skills taxonomy JSON file
        """
        self.skills_taxonomy = self._load_skills_taxonomy(skills_file)
        self.all_skills = self._flatten_skills_taxonomy()
        self.stop_words = set(stopwords.words('english'))
    
    def _load_skills_taxonomy(self, skills_file: str = None) -> dict:
        """Load skills taxonomy from JSON file."""
        if skills_file is None:
            skills_file = Path(__file__).parent.parent / "data" / "skills.json"
        
        try:
            with open(skills_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Could not load skills from {skills_file}: {e}")
            return self._get_default_skills()
    
    def _get_default_skills(self) -> dict:
        """Return a default minimal skill taxonomy."""
        return {
            "programming_languages": ["python", "java", "javascript", "c++", "c#", "php", "ruby", "go", "rust", "kotlin"],
            "web_frameworks": ["django", "flask", "fastapi", "react", "angular", "vue", "express", "spring"],
            "databases": ["sql", "mysql", "postgresql", "mongodb", "oracle", "redis", "cassandra"],
            "cloud": ["aws", "azure", "gcp", "google cloud", "kubernetes", "docker", "gke"],
            "data_science": ["pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "r", "spark"],
            "tools": ["git", "jira", "linux", "unix", "agile", "scrum"]
        }
    
    def _flatten_skills_taxonomy(self) -> Dict[str, str]:
        """
        Flatten taxonomy into {skill: category} mapping.
        Example: {"python": "programming_languages", ...}
        """
        flattened = {}
        for category, skills in self.skills_taxonomy.items():
            for skill in skills:
                flattened[skill.lower()] = category
        return flattened
    
    def extract_skills(self, text: str, threshold: int = 1) -> dict:
        """
        Extract skills from text.
        
        Args:
            text: Input text (resume or JD)
            threshold: Minimum occurrences to count as matched
            
        Returns:
            Dictionary with found skills by category and their frequencies
        """
        text_lower = text.lower()
        skills_found = {}
        skill_frequencies = {}
        
        for skill in self.all_skills.keys():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            matches = re.findall(pattern, text_lower)
            count = len(matches)
            
            if count >= threshold:
                category = self.all_skills[skill]
                if category not in skills_found:
                    skills_found[category] = []
                skills_found[category].append(skill)
                skill_frequencies[skill] = count
        
        return {
            "by_category": skills_found,
            "frequencies": skill_frequencies,
            "total_unique": len(skill_frequencies)
        }


def preprocess_text(text: str) -> str:
    """
    Preprocess text for NLP: lowercase, remove special chars, etc.
    
    Args:
        text: Raw text
        
    Returns:
        Preprocessed text
    """
    # Lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Remove email-like patterns (but not the @ symbol if we need it)
    text = re.sub(r'\S+@\S+', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def tokenize_text(text: str) -> List[str]:
    """
    Tokenize text into words.
    
    Args:
        text: Input text
        
    Returns:
        List of word tokens
    """
    return word_tokenize(text.lower())


def get_sentences(text: str) -> List[str]:
    """
    Split text into sentences.
    
    Args:
        text: Input text
        
    Returns:
        List of sentences
    """
    try:
        return sent_tokenize(text)
    except Exception as e:
        logger.warning(f"Error tokenizing into sentences: {e}")
        return text.split('. ')


def extract_keywords(text: str, top_n: int = 20) -> List[str]:
    """
    Extract top keywords from text (excluding stopwords).
    
    Args:
        text: Input text
        top_n: Number of top keywords to return
        
    Returns:
        List of top keywords
    """
    stop_words = set(stopwords.words('english'))
    tokens = tokenize_text(text)
    
    # Filter stopwords and short tokens
    keywords = [token for token in tokens if token.isalnum() and token not in stop_words and len(token) > 2]
    
    # Count frequencies
    from collections import Counter
    freq_dist = Counter(keywords)
    
    # Return top N
    top_keywords = [word for word, _ in freq_dist.most_common(top_n)]
    return top_keywords
