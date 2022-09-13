import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/database.sqlite"
    CSRF_SECRET_KEY = os.environ.get("CSRF_SECRET_KEY").encode()
