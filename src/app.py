from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
import qrcode
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Update this
app.config['MAIL_PASSWORD'] = 'your-app-password'     # Update this

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    two_factor_secret = db.Column(db.String(32))
    two_factor_type = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('signup'))
        
        session['temp_user'] = {
            'username': username,
            'email': email,
            'password': password
        }
        return redirect(url_for('setup_2fa'))
    
    return render_template('signup.html')

@app.route('/setup-2fa', methods=['GET', 'POST'])
def setup_2fa():
    if 'temp_user' not in session:
        return redirect(url_for('signup'))
    
    if request.method == 'POST':
        two_factor_type = request.form.get('2fa_type')
        user_data = session['temp_user']
        
        if two_factor_type == 'authenticator':
            secret = pyotp.random_base32()
            totp = pyotp.TOTP(secret)
            provisioning_uri = totp.provisioning_uri(
                user_data['email'],
                issuer_name="Your App Name"
            )
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(provisioning_uri)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            qr_code = base64.b64encode(buffered.getvalue()).decode()
            
            session['temp_user']['two_factor_secret'] = secret
            session['temp_user']['two_factor_type'] = 'authenticator'
            
            return render_template('setup_authenticator.html', 
                                qr_code=qr_code, 
                                secret=secret)
        
        elif two_factor_type == 'email':
            secret = pyotp.random_base32()
            totp = pyotp.TOTP(secret)
            code = totp.now()
            
            session['temp_user']['two_factor_secret'] = secret
            session['temp_user']['two_factor_type'] = 'email'
            
            msg = Message('Your Verification Code',
                         sender=app.config['MAIL_USERNAME'],
                         recipients=[user_data['email']])
            msg.body = f'Your verification code is: {code}'
            mail.send(msg)
            
            return render_template('verify_email_2fa.html')
    
    return render_template('setup_2fa.html')

@app.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    if 'temp_user' not in session:
        return redirect(url_for('signup'))
    
    code = request.form.get('code')
    user_data = session['temp_user']
    
    if pyotp.TOTP(user_data['two_factor_secret']).verify(code):
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            two_factor_secret=user_data['two_factor_secret'],
            two_factor_type=user_data['two_factor_type']
        )
        user.set_password(user_data['password'])
        db.session.add(user)
        db.session.commit()
        
        session.pop('temp_user', None)
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    flash('Invalid verification code')
    return redirect(url_for('setup_2fa'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
            
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)