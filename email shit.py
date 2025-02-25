from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, decode_token
import secrets
import smtplib
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer
import datetime

app = Flask(__name__)

# Database configuration (Use SQLite for simplicity, replace with PostgreSQL/MySQL)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)

# Secret key for generating tokens
SECRET_KEY = "your-secret-key"
serializer = URLSafeTimedSerializer(SECRET_KEY)

# Email settings
SENDER_EMAIL = "your-email@gmail.com"
APP_PASSWORD = "your-app-password"  # Use an App Password (not your real password)


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)


# Create database
with app.app_context():
    db.create_all()


# Function to send email with login link
def send_login_email(user_email, token):
    login_link = f"http://127.0.0.1:5000/confirm-login?token={token}"
    msg = MIMEText(f"Click the link to log in: {login_link}")
    msg["Subject"] = "Your Login Link"
    msg["From"] = SENDER_EMAIL
    msg["To"] = user_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, user_email, msg.as_string())


# Route to request login
@app.route("/request-login", methods=["POST"])
def request_login():
    data = request.json
    email = data.get("email")

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Generate a unique token that expires in 5 minutes
    token = serializer.dumps(email, salt="email-confirmation")

    # Send email with login link
    send_login_email(email, token)

    return jsonify({"message": "Check your email for the login link."})


# Route to confirm login
@app.route("/confirm-login")
def confirm_login():
    token = request.args.get("token")

    try:
        email = serializer.loads(token, salt="email-confirmation", max_age=300)  # Token expires in 5 minutes

        # Generate a JWT token for session management
        access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(hours=1))

        return jsonify({"message": "Login successful!", "token": access_token})

    except Exception as e:
        return jsonify({"error": "Invalid or expired token"}), 401


if __name__ == "__main__":
    app.run(debug=True)


app = Flask(__name__)

# Database configuration (Use SQLite for simplicity, replace with PostgreSQL/MySQL)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)

# Secret key for generating tokens
SECRET_KEY = "your-secret-key"
serializer = URLSafeTimedSerializer(SECRET_KEY)

# Email settings
SENDER_EMAIL = "your-email@gmail.com"
APP_PASSWORD = "your-app-password"  # Use an App Password (not your real password)


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)


# Create database
with app.app_context():
    db.create_all()


# Function to send email with login link
def send_login_email(user_email, token):
    login_link = f"http://127.0.0.1:5000/confirm-login?token={token}"
    msg = MIMEText(f"Click the link to log in: {login_link}")
    msg["Subject"] = "Your Login Link"
    msg["From"] = SENDER_EMAIL
    msg["To"] = user_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, user_email, msg.as_string())


# Route to request login
@app.route("/request-login", methods=["POST"])
def request_login():
    data = request.json
    email = data.get("email")

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Generate a unique token that expires in 5 minutes
    token = serializer.dumps(email, salt="email-confirmation")

    # Send email with login link
    send_login_email(email, token)

    return jsonify({"message": "Check your email for the login link."})


# Route to confirm login
@app.route("/confirm-login")
def confirm_login():
    token = request.args.get("token")

    try:
        email = serializer.loads(token, salt="email-confirmation", max_age=300)  # Token expires in 5 minutes

        # Generate a JWT token for session management
        access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(hours=1))

        return jsonify({"message": "Login successful!", "token": access_token})

    except Exception as e:
        return jsonify({"error": "Invalid or expired token"}), 401


if __name__ == "__main__":
    app.run(debug=True)
