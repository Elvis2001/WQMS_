import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.app_context().push()

# Configuration
app.config['SECRET_KEY'] = 'helloworld'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_NAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

# Initialize extensions
mail = Mail(app)
db = SQLAlchemy(app)

# Import routes
from WQMS import routes, routes2
