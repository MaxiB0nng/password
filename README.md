# Flask Authentication Dashboard

This project is a Flask web application that provides a user authentication system with login and signup functionality. It features a dashboard for registered users and is styled using Bootstrap.

## Project Structure

```
flask-auth-app
├── src
│   ├── app.py                # Main entry point of the Flask application
│   ├── models.py             # Database models using SQLAlchemy
│   ├── database.py           # Database connection and setup
│   ├── config.py             # Configuration settings for the application
│   ├── static
│   │   ├── css
│   │   │   └── style.css     # Custom CSS styles
│   │   └── js
│   │       └── main.js       # JavaScript for client-side functionality
│   └── templates
│       ├── base.html         # Base HTML template
│       ├── login.html        # User login form
│       ├── signup.html       # User registration form
│       └── dashboard.html     # User dashboard
├── requirements.txt           # Project dependencies
├── .env                       # Environment variables
└── README.md                  # Project documentation
```

## Features

- User registration and login
- User dashboard displaying user-specific information
- Responsive design using Bootstrap
- Secure password handling with hashing

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-auth-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the environment variables in the `.env` file:
   ```
   DATABASE_URL=<your-database-url>
   SECRET_KEY=<your-secret-key>
   ```

5. Run the application:
   ```
   python src/app.py
   ```

6. Access the application in your web browser at `http://127.0.0.1:5000`.

## Usage

- Navigate to the signup page to create a new account.
- After registration, log in to access the dashboard.
- The dashboard displays user-specific information and options.

## License

This project is licensed under the MIT License.