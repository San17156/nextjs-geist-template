#!/usr/bin/env python3
"""
Smart Recruitment System - Main Application Entry Point
"""

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import blueprints
from services.file_processor import file_bp
from services.nlp_engine import nlp_bp
from services.ml_matcher import ml_bp
from services.recommendation import rec_bp

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configure app
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'src/data/uploads')
    app.config['PROCESSED_FOLDER'] = os.getenv('PROCESSED_FOLDER', 'src/data/processed')
    
    # Register blueprints
    app.register_blueprint(file_bp, url_prefix='/api/files')
    app.register_blueprint(nlp_bp, url_prefix='/api/nlp')
    app.register_blueprint(ml_bp, url_prefix='/api/ml')
    app.register_blueprint(rec_bp, url_prefix='/api/recommendations')
    
    # Health check endpoint
    @app.route('/')
    def index():
        return {'message': 'Smart Recruitment System API. See README for usage.'}

    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'smart-recruitment-system'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    )
