class Config:
    SECRET_KEY = 'your-secret-key'  # Change this to a random secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False