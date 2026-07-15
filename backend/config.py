import os

class Config:
    # Assuming a default local MySQL setup (XAMPP/WAMP) where root has no password.
    # The database named 'visionedge' must be created beforehand in MySQL: CREATE DATABASE visionedge;
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@localhost/visionedge'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret Keys
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-visionedge-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-super-secret-signature'
