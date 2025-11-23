"""
Utility functions
"""
import logging
from pathlib import Path

def setup_logging(log_level=logging.INFO):
    """Setup logging configuration"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'chroma_db', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)