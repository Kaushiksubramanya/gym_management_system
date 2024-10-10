from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

# User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Member model
class Member(db.Model):
    __tablename__ = 'members'  # Change from 'member' to 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
   # gender = db.Column(db.String(10), nullable=False)  # Add gender column
    age = db.Column(db.Integer, nullable=False)
    phoneNo = db.Column(db.String(15), nullable=False)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    emergency_contact = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    #membership_package = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Member {self.name}>'
