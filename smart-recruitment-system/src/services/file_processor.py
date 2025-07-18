"""
File Processing Service
"""

import os
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import PyPDF2
from docx import Document
import magic

file_bp = Blueprint('file_processor', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")

@file_bp.route('/upload-resumes', methods=['POST'])
def upload_resumes():
    """Upload and process multiple resumes"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        processed_files = []
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_id = str(uuid.uuid4())
                file_path = os.path.join(file_bp.root_path, 'data/uploads', f"{file_id}_{filename}")
                
                # Save file
                file.save(file_path)
                
                # Extract text based on file type
                file_extension = filename.rsplit('.', 1)[1].lower()
                
                if file_extension == 'pdf':
                    text = extract_text_from_pdf(file_path)
                elif file_extension in ['docx', 'doc']:
                    text = extract_text_from_docx(file_path)
                else:
                    continue
                
                processed_files.append({
                    'file_id': file_id,
                    'filename': filename,
                    'file_type': file_extension,
                    'extracted_text': text,
                    'file_path': file_path
                })
        
        return jsonify({
            'message': f'Processed {len(processed_files)} files',
            'files': processed_files
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@file_bp.route('/upload-jobs', methods=['POST'])
def upload_jobs():
    """Upload job postings in JSON format"""
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        jobs_data = request.get_json()
        
        if not isinstance(jobs_data, list):
            return jsonify({'error': 'Expected a list of job postings'}), 400
        
        processed_jobs = []
        for job_data in jobs_data:
            # Validate required fields
            required_fields = ['job_id', 'title', 'description', 'requirements']
            if not all(field in job_data for field in required_fields):
                continue
            
            processed_jobs.append(job_data)
        
        return jsonify({
            'message': f'Processed {len(processed_jobs)} job postings',
            'jobs': processed_jobs
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
