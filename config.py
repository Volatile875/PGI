import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_POOL_SIZE = int(os.environ.get("DB_MAX_POOL", 10))
    DB_POOL_MIN = int(os.environ.get("DB_MIN_POOL", 2))
    
    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FORMAT = os.environ.get("LOG_FORMAT", "json")
    LOG_DIR = BASE_DIR / "logs"
    
    # Feature Flags
    SQL_SAFETY_STRICT_MODE = os.environ.get("SQL_SAFETY_STRICT_MODE", "true").lower() == "true"
    
    @staticmethod
    def init_app(app):
        # Create logs directory if it doesn't exist
        if not os.path.exists(Config.LOG_DIR):
            os.makedirs(Config.LOG_DIR)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # In production, we expect DATABASE_URL to be set strictly
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}

def get_config():
    env = os.environ.get("FLASK_ENV", "development").lower()
    return config_by_name.get(env, DevelopmentConfig)
