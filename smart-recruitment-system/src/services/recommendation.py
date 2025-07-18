"""
Recommendation Service
"""

from flask import Blueprint, request, jsonify
from typing import List, Dict, Any

rec_bp = Blueprint('recommendation', __name__)

class RecommendationEngine:
    """Generate recommendations based on match scores"""
    
    def __init__(self):
        self.min_match_threshold = 0.3
    
    def get_top_candidates(self, matches: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
        """Get top N candidates based on match scores"""
        # Filter by minimum threshold
        filtered_matches = [m for m in matches if m.get('overall_match_score', 0) >= self.min_match_threshold]
        
        # Sort by overall match score
        sorted_matches = sorted(filtered_matches, key=lambda x: x.get('overall_match_score', 0), reverse=True)
        
        # Limit results
        return sorted_matches[:limit]
    
    def generate_recommendation_report(self, matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate detailed recommendation report"""
        if not matches:
            return {
                'total_candidates': 0,
                'recommendations': [],
                'summary': {}
            }
        
        # Categorize recommendations
        highly_recommended = [m for m in matches if m.get('overall_match_score', 0) >= 0.8]
        recommended = [m for m in matches if 0.6 <= m.get('overall_match_score', 0) < 0.8]
        consider = [m for m in matches if 0.4 <= m.get('overall_match_score', 0) < 0.6]
        
        summary = {
            'total_candidates': len(matches),
            'highly_recommended': len(highly_recommended),
            'recommended': len(recommended),
            'consider': len(consider),
            'average_score': sum(m.get('overall_match_score', 0) for m in matches) / len(matches)
        }
        
        return {
            'summary': summary,
            'recommendations': matches,
            'categories': {
                'highly_recommended': highly_recommended,
                'recommended': recommended,
                'consider': consider
            }
        }

# Initialize recommendation engine
rec_engine = RecommendationEngine()

@rec_bp.route('/top-candidates/<job_id>', methods=['GET'])
def get_top_candidates(job_id):
    """Get top candidates for a specific job"""
    try:
        limit = int(request.args.get('limit', 10))
        
        # In a real implementation, this would fetch from database
        # For now, we'll use mock data
        mock_matches = [
            {
                'job_id': job_id,
                'candidate_id': 'candidate_001',
                'name': 'John Doe',
                'overall_match_score': 0.85,
                'skill_match_score': 0.9,
                'experience_match_score': 0.8,
                'education_match_score': 0.85,
                'matched_skills': ['python', 'machine learning', 'sql'],
                'missing_skills': ['kubernetes']
            },
            {
                'job_id': job_id,
                'candidate_id': 'candidate_002',
                'name': 'Jane Smith',
                'overall_match_score': 0.78,
                'skill_match_score': 0.85,
                'experience_match_score': 0.75,
                'education_match_score': 0.8,
                'matched_skills': ['python', 'data science', 'pandas'],
                'missing_skills': ['docker', 'kubernetes']
            }
        ]
        
        top_candidates = rec_engine.get_top_candidates(mock_matches, limit)
        
        return jsonify({
            'job_id': job_id,
            'top_candidates': top_candidates,
            'total_found': len(top_candidates)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rec_bp.route('/report/<job_id>', methods=['GET'])
def get_recommendation_report(job_id):
    """Get detailed recommendation report for a job"""
    try:
        # In a real implementation, this would fetch from database
        mock_matches = [
            {
                'job_id': job_id,
                'candidate_id': 'candidate_001',
                'name': 'John Doe',
                'overall_match_score': 0.85,
                'skill_match_score': 0.9,
                'experience_match_score': 0.8,
                'education_match_score': 0.85,
                'matched_skills': ['python', 'machine learning', 'sql'],
                'missing_skills': ['kubernetes']
            },
            {
                'job_id': job_id,
                'candidate_id': 'candidate_002',
                'name': 'Jane Smith',
                'overall_match_score': 0.78,
                'skill_match_score': 0.85,
                'experience_match_score': 0.75,
                'education_match_score': 0.8,
                'matched_skills': ['python', 'data science', 'pandas'],
                'missing_skills': ['docker', 'kubernetes']
            },
            {
                'job_id': job_id,
                'candidate_id': 'candidate_003',
                'name': 'Bob Johnson',
                'overall_match_score': 0.65,
                'skill_match_score': 0.7,
                'experience_match_score': 0.6,
                'education_match_score': 0.7,
                'matched_skills': ['java', 'spring', 'sql'],
                'missing_skills': ['python', 'machine learning']
            }
        ]
        
        report = rec_engine.generate_recommendation_report(mock_matches)
        
        return jsonify(report), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
