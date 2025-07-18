#!/usr/bin/env python3
"""
Simple startup script for Smart Recruitment System
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import create_app

if __name__ == '__main__':
    app = create_app()
    print("Starting Smart Recruitment System...")
    print("Available at: http://localhost:5000")
    print("Health check: http://localhost:5000/health")
    print("API docs: See README.md")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
