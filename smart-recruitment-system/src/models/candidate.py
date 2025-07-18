"""
Candidate Data Model
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class Candidate:
    """Data model for candidates"""
    candidate_id: str
    name: str
    email: str
    phone: str = ""
    skills: List[str] = None
    experience: List[Dict[str, Any]] = None
    education: List[Dict[str, Any]] = None
    resume_text: str = ""
    processed_keywords: List[str] = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.skills is None:
            self.skills = []
        if self.experience is None:
            self.experience = []
        if self.education is None:
            self.education = []
        if self.processed_keywords is None:
            self.processed_keywords = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'candidate_id': self.candidate_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'skills': self.skills,
            'experience': self.experience,
            'education': self.education,
            'resume_text': self.resume_text,
            'processed_keywords': self.processed_keywords
        }
    
    def add_skill(self, skill: str):
        """Add a skill to the candidate's profile"""
        if skill and skill not in self.skills:
            self.skills.append(skill)
    
    def add_experience(self, company: str, role: str, duration: str, description: str = ""):
        """Add work experience"""
        self.experience.append({
            'company': company,
            'role': role,
            'duration': duration,
            'description': description
        })
    
    def add_education(self, degree: str, institution: str, year: str, gpa: str = ""):
        """Add education details"""
        self.education.append({
            'degree': degree,
            'institution': institution,
            'year': year,
            'gpa': gpa
        })
