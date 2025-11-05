import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # PostgreSQL database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://iantu@localhost:5432/camping_fun'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Set to False in production
    JSON_SORT_KEYS = False