"""
Scoring and matching module for resume-to-JD comparison.
Uses TF-IDF and keyword matching for scoring.
"""

import logging
from typing import Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class ResumeMatcher:
    """Match resume to job description and generate scores."""
    
    def __init__(self):
        """Initialize the matcher."""
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            max_features=500,
            ngram_range=(1, 2)
        )
    
    def calculate_similarity_score(self, resume_text: str, jd_text: str) -> float:
        """
        Calculate TF-IDF cosine similarity between resume and JD.
        
        Args:
            resume_text: Resume text
            jd_text: Job description text
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            # Combine texts and fit vectorizer
            texts = [resume_text, jd_text]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def calculate_skill_match_score(self, resume_skills: dict, jd_skills: dict) -> Tuple[float, Dict]:
        """
        Calculate skill match score based on extracted skills.
        
        Args:
            resume_skills: Skills extracted from resume (from SkillExtractor)
            jd_skills: Skills extracted from JD (from SkillExtractor)
            
        Returns:
            Tuple of (score: float, details: dict)
        """
        resume_flat = set()
        jd_flat = set()
        
        # Flatten resume skills
        for category, skills in resume_skills.get("by_category", {}).items():
            resume_flat.update(skills)
        
        # Flatten JD skills
        for category, skills in jd_skills.get("by_category", {}).items():
            jd_flat.update(skills)
        
        if not jd_flat:
            # No skills required in JD
            return 1.0, {"matched": [], "missing": [], "required": 0}
        
        # Calculate intersection
        matched = resume_flat & jd_flat
        missing = jd_flat - resume_flat
        
        # Score: ratio of matched to required
        score = len(matched) / len(jd_flat) if jd_flat else 0.0
        
        return float(score), {
            "matched": sorted(list(matched)),
            "missing": sorted(list(missing)),
            "required": len(jd_flat),
            "found": len(resume_flat)
        }
    
    def generate_composite_score(self, 
                                 similarity_score: float, 
                                 skill_match_score: float,
                                 weights: dict = None) -> float:
        """
        Generate composite score from multiple factors.
        
        Args:
            similarity_score: TF-IDF similarity (0-1)
            skill_match_score: Skill match ratio (0-1)
            weights: Dict with 'similarity' and 'skills' weights (default: equal)
            
        Returns:
            Composite score (0-100)
        """
        if weights is None:
            weights = {"similarity": 0.5, "skills": 0.5}
        
        composite = (similarity_score * weights["similarity"] + 
                    skill_match_score * weights["skills"])
        
        return composite * 100
    
    def generate_feedback(self, 
                         resume_text: str,
                         jd_text: str,
                         skill_match_details: dict,
                         composite_score: float) -> str:
        """
        Generate human-readable feedback based on scoring.
        
        Args:
            resume_text: Resume text
            jd_text: Job description text
            skill_match_details: Skill matching details
            composite_score: Overall composite score (0-100)
            
        Returns:
            Feedback string
        """
        feedback = []
        
        # Overall assessment
        if composite_score >= 80:
            feedback.append("✓ Excellent match! This resume aligns well with the job requirements.")
        elif composite_score >= 60:
            feedback.append("○ Good match. The candidate has relevant skills and experience.")
        elif composite_score >= 40:
            feedback.append("⚠ Partial match. The candidate has some relevant skills but may lack others.")
        else:
            feedback.append("✗ Limited match. Consider looking for candidates with more aligned experience.")
        
        # Skill feedback
        matched = skill_match_details.get("matched", [])
        missing = skill_match_details.get("missing", [])
        required = skill_match_details.get("required", 0)
        found = skill_match_details.get("found", 0)
        
        if matched:
            feedback.append(f"\nMatched Skills: {', '.join(matched[:5])}" + 
                          (f" (+{len(matched)-5} more)" if len(matched) > 5 else ""))
        
        if missing:
            feedback.append(f"\nMissing Skills: {', '.join(missing[:3])}" + 
                          (f" (+{len(missing)-3} more)" if len(missing) > 3 else ""))
        
        feedback.append(f"\nSkill Coverage: {found}/{required} total skills found" if required else 
                       f"\nResume includes {found} relevant skills")
        
        # Length feedback
        resume_words = len(resume_text.split())
        if resume_words < 100:
            feedback.append("\nNote: Resume is quite short. Consider adding more details.")
        elif resume_words > 1500:
            feedback.append("\nNote: Resume is very long. Consider condensing to 1-2 pages.")
        
        return "\n".join(feedback)
    
    def score_resume(self, 
                    resume_text: str, 
                    jd_text: str,
                    resume_skills: dict,
                    jd_skills: dict,
                    weights: dict = None) -> dict:
        """
        Complete scoring pipeline for a resume against a JD.
        
        Args:
            resume_text: Resume text
            jd_text: Job description text
            resume_skills: Extracted skills from resume
            jd_skills: Extracted skills from JD
            weights: Scoring weights
            
        Returns:
            Complete scoring result dict
        """
        # Calculate similarity score
        similarity = self.calculate_similarity_score(resume_text, jd_text)
        
        # Calculate skill match score
        skill_match, skill_details = self.calculate_skill_match_score(resume_skills, jd_skills)
        
        # Generate composite score
        composite = self.generate_composite_score(similarity, skill_match, weights)
        
        # Generate feedback
        feedback = self.generate_feedback(resume_text, jd_text, skill_details, composite)
        
        return {
            "final_score": round(composite, 2),
            "similarity_score": round(similarity * 100, 2),
            "skill_match_score": round(skill_match * 100, 2),
            "skill_details": skill_details,
            "feedback": feedback,
            "rating": self._score_to_rating(composite)
        }
    
    def _score_to_rating(self, score: float) -> str:
        """Convert numeric score to star rating."""
        if score >= 80:
            return "⭐⭐⭐⭐⭐"
        elif score >= 60:
            return "⭐⭐⭐⭐"
        elif score >= 40:
            return "⭐⭐⭐"
        elif score >= 20:
            return "⭐⭐"
        else:
            return "⭐"
