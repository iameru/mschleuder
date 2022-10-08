from dotenv import dotenv_values

env = dotenv_values(".env")


class Config:

    SECRET_KEY = env.get("SECRET_KEY")
    CSRF_SECRET_KEY = env.get("CSRF_SECRET_KEY").encode()

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = env.get("DATABASE_URL")
