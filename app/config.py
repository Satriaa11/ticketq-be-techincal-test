from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tickets.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration dengan algoritma HS256
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string-change-in-production'
    JWT_ALGORITHM = 'HS256'  # Algoritma yang digunakan
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Token pendek
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)    # Refresh token lebih lama

    # JWT Additional Settings
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ERROR_MESSAGE_KEY = 'message'

    # JWT Header Configuration
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # JWT Claims
    JWT_IDENTITY_CLAIM = 'sub'
    JWT_USER_CLAIMS = 'user_claims'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///revobank_dev.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}