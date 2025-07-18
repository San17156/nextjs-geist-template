"""
Configuration utilities
"""

import os
from typing import Dict, Any

class Config:
    """Application configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'src/data/uploads')
    PROCESSED_FOLDER = os.getenv('PROCESSED_FOLDER', 'src/data/processed')
    
    # API Configuration
    API_VERSION = os.getenv('API_VERSION', 'v1')
    API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', 100))
    
    # ML Configuration
    MIN_MATCH_THRESHOLD = float(os.getenv('MIN_MATCH_THRESHOLD', 0.3))
    MAX_RECOMMENDATIONS = int(os.getenv('MAX_RECOMMENDATIONS', 10))
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'max_content_length': cls.MAX_CONTENT_LENGTH,
            'upload_folder': cls.UPLOAD_FOLDER,
            'processed_folder': cls.PROCESSED_FOLDER,
            'api_version': cls.API_VERSION,
            'min_match_threshold': cls.MIN_MATCH_THRESHOLD,
            'max_recommendations': cls.MAX_RECOMMENDATIONS
        }
