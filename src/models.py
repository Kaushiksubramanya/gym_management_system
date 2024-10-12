from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize the database
db = SQLAlchemy()

# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # role = 'admin'
    is_active = db.Column(db.Boolean, default=False) 
        # Flask-Login required methods
    def is_authenticated(self):
        return True

    def is_active(self):
        return True  # Can be used to block users, return False if user is inactive

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # Needs to return a string, not an int

    def __repr__(self):
        return f'<User {self.username}>'

# Member model
class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phoneNo = db.Column(db.String(15), nullable=False)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    emergency_contact = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    membership_package = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Member {self.name}>'
