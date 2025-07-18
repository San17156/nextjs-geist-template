"""
Match Result Data Model
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class MatchResult:
    """Data model for match results between job and candidate"""
    job_id: str
    candidate_id: str
    match_score: float
    skill_match_score: float
    experience_match_score: float
    education_match_score: float
    overall_match_score: float
    matched_skills: list
    missing_skills: list
    explanation: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'job_id': self.job_id,
            'candidate_id': self.candidate_id,
            'match_score': self.match_score,
            'skill_match_score': self.skill_match_score,
            'experience_match_score': self.experience_match_score,
            'education_match_score': self.education_match_score,
            'overall_match_score': self.overall_match_score,
            'matched_skills': self.matched_skills,
            'missing_skills': self.missing_skills,
            'explanation': self.explanation
        }
    
    def get_recommendation_level(self) -> str:
        """Get recommendation level based on match score"""
        if self.overall_match_score >= 0.8:
            return "Highly Recommended"
        elif self.overall_match_score >= 0.6:
            return "Recommended"
        elif self.overall_match_score >= 0.4:
            return "Consider"
        else:
            return "Not Recommended"
