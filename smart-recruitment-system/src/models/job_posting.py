"""
Job Posting Data Model
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import json

@dataclass
class JobPosting:
    """Data model for job postings"""
    job_id: str
    title: str
    description: str
    requirements: Dict[str, Any]
    salary_range: Dict[str, float]
    company: str = ""
    location: str = ""
    posted_date: str = ""
    
    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> 'JobPosting':
        """Create JobPosting from JSON data"""
        return cls(
            job_id=json_data.get('job_id', ''),
            title=json_data.get('title', ''),
            description=json_data.get('description', ''),
            requirements=json_data.get('requirements', {}),
            salary_range=json_data.get('salary_range', {}),
            company=json_data.get('company', ''),
            location=json_data.get('location', ''),
            posted_date=json_data.get('posted_date', '')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'job_id': self.job_id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'salary_range': self.salary_range,
            'company': self.company,
            'location': self.location,
            'posted_date': self.posted_date
        }
    
    def get_required_skills(self) -> List[str]:
        """Extract required skills from requirements"""
        return self.requirements.get('skills', [])
    
    def get_required_experience(self) -> str:
        """Get required experience"""
        return self.requirements.get('experience', "")
    
    def get_required_education(self) -> str:
        """Get required education"""
        return self.requirements.get('education', "")
