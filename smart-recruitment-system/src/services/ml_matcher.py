"""
ML Matching Service
"""

import numpy as np
from flask import Blueprint, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any

ml_bp = Blueprint('ml_matcher', __name__)

class MLMatcher:
    """ML-based job-candidate matching engine"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
    def calculate_similarity(self, job_text: str, candidate_text: str) -> float:
        """Calculate similarity between job and candidate"""
        try:
            # Create TF-IDF vectors
            vectors = self.vectorizer.fit_transform([job_text, candidate_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            
            return float(similarity)
        
        except Exception as e:
            return 0.0
    
    def match_job_with_candidates(self, job_data: Dict[str, Any], candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Match a job with multiple candidates"""
        job_text = f"{job_data.get('title', '')} {job_data.get('description', '')}"
        job_skills = job_data.get('requirements', {}).get('skills', [])
        
        matches = []
        
        for candidate in candidates:
            candidate_text = candidate.get('resume_text', '')
            candidate_skills = candidate.get('skills', [])
            
            # Calculate overall similarity
            overall_similarity = self.calculate_similarity(job_text, candidate_text)
            
            # Calculate skill match
            skill_matches = set(job_skills).intersection(set(candidate_skills))
            skill_match_score = len(skill_matches) / len(job_skills) if job_skills else 0
            
            # Calculate experience match (simplified)
            experience_match_score = 0.5  # Placeholder
            
            # Calculate education match (simplified)
            education_match_score = 0.5  # Placeholder
            
            # Overall match score
            overall_match_score = (
                overall_similarity * 0.4 +
                skill_match_score * 0.4 +
                experience_match_score * 0.1 +
                education_match_score * 0.1
            )
            
            matches.append({
                'job_id': job_data.get('job_id'),
                'candidate_id': candidate.get('candidate_id'),
                'match_score': overall_similarity,
                'skill_match_score': skill_match_score,
                'experience_match_score': experience_match_score,
                'education_match_score': education_match_score,
                'overall_match_score': overall_match_score,
                'matched_skills': list(skill_matches),
                'missing_skills': list(set(job_skills) - set(candidate_skills))
            })
        
        # Sort by overall match score
        matches.sort(key=lambda x: x['overall_match_score'], reverse=True)
        
        return matches

# Initialize matcher
matcher = MLMatcher()

@ml_bp.route('/match', methods=['POST'])
def match_candidates():
    """Match candidates with job requirements"""
    try:
        data = request.get_json()
        job_data = data.get('job')
        candidates = data.get('candidates', [])
        
        if not job_data or not candidates:
            return jsonify({'error': 'Job data and candidates are required'}), 400
        
        matches = matcher.match_job_with_candidates(job_data, candidates)
        
        return jsonify({
            'job_id': job_data.get('job_id'),
            'total_candidates': len(candidates),
            'matches': matches
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ml_bp.route('/similarity', methods=['POST'])
def calculate_similarity_endpoint():
    """Calculate similarity between two texts"""
    try:
        data = request.get_json()
        text1 = data.get('text1', '')
        text2 = data.get('text2', '')
        
        if not text1 or not text2:
            return jsonify({'error': 'Both texts are required'}), 400
        
        similarity = matcher.calculate_similarity(text1, text2)
        
        return jsonify({
            'text1': text1[:100] + '...' if len(text1) > 100 else text1,
            'text2': text2[:100] + '...' if len(text2) > 100 else text2,
            'similarity_score': similarity
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
