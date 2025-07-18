# Smart Recruitment System

A Python-based Smart Recruitment System that uses ML and NLP to automatically match job postings with candidate resumes.

## Features

- **Bulk Job Posting Upload**: Upload multiple job postings in JSON format
- **Resume Processing**: Process PDF, DOCX, and DOC resume files
- **ML/NLP Matching**: Use machine learning and NLP to match candidates with job requirements
- **Automated Recommendations**: Get ranked list of top candidates
- **Detailed Reports**: Comprehensive match analysis and recommendations

## Architecture

```
smart-recruitment-system/
├── src/
│   ├── main.py                 # Entry point
│   ├── models/                 # Data models
│   ├── services/               # Core services
│   ├── utils/                  # Utilities
│   └── data/                   # Data storage
├── tests/                      # Test files
├── docs/                       # Documentation
└── requirements.txt            # Dependencies
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd smart-recruitment-system
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. Run the application:
```bash
python src/main.py
```

## Usage

### Upload Job Postings
```json
POST /api/files/upload-jobs
[
  {
    "job_id": "job_001",
    "title": "Senior Python Developer",
    "description": "We are looking for a senior Python developer...",
    "requirements": {
      "skills": ["python", "django", "postgresql"],
      "experience": "5+ years",
      "education": "Bachelor's degree"
    },
    "salary_range": {"min": 80000, "max": 120000}
  }
]
```

### Upload Resumes
```bash
curl -X POST http://localhost:5000/api/files/upload-resumes \
  -F "files=@resume1.pdf" \
  -F "files=@resume2.docx"
```

### Get Recommendations
```bash
curl http://localhost:5000/api/recommendations/top-candidates/job_001?limit=5
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
