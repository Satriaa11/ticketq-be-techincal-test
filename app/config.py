import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class for TicketQ API"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tickets.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API Configuration
    API_TITLE = os.environ.get('API_TITLE') or "TicketQ API"
    API_VERSION = os.environ.get('API_VERSION') or "1.0.0"
    API_DESCRIPTION = "Simple Ticket Management API"

    # Environment
    ENV = os.environ.get('ENV') or 'development'

class DevelopmentConfig(Config):
    DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tickets_dev.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tickets_test.db'

class ProductionConfig(Config):
    DEBUG = False

    def __init__(self):
        super().__init__()
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL must be set in production")
        self.SQLALCHEMY_DATABASE_URI = database_url

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}