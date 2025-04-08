import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///expenses.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
