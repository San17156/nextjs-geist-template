"""
NLP Processing Service
"""

import re
import nltk
from flask import Blueprint, request, jsonify
from typing import List, Dict, Any
import spacy

nlp_bp = Blueprint('nlp_engine', __name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

@nlp_bp.route('/preprocess-text', methods=['POST'])
def preprocess_text():
    """Preprocess text for NLP analysis"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Clean text
        cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
        
        # Tokenize
        tokens = word_tokenize(cleaned_text)
        
        # Remove stopwords and lemmatize
        processed_tokens = [
            lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in stop_words and len(token) > 2
        ]
        
        return jsonify({
            'original_text': text,
            'processed_tokens': processed_tokens,
            'token_count': len(processed_tokens)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nlp_bp.route('/extract-keywords', methods=['POST'])
def extract_keywords():
    """Extract keywords from text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Simple keyword extraction based on frequency
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = {}
        
        for word in words:
            if word not in stop_words and len(word) > 2:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top keywords
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        
        return jsonify({
            'keywords': [kw[0] for kw in top_keywords],
            'keyword_frequencies': dict(top_keywords)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nlp_bp.route('/extract-skills', methods=['POST'])
def extract_skills():
    """Extract skills from resume text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Common technical skills list (simplified)
        technical_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'machine learning', 'deep learning', 'ai', 'nlp',
            'data science', 'data analysis', 'pandas', 'numpy', 'scikit-learn', 'tensorflow',
            'pytorch', 'git', 'linux', 'agile', 'scrum', 'rest api', 'microservices'
        ]
        
        # Extract skills from text
        text_lower = text.lower()
        found_skills = [skill for skill in technical_skills if skill in text_lower]
        
        return jsonify({
            'extracted_skills': found_skills,
            'skill_count': len(found_skills)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
