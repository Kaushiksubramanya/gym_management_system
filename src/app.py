from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db, Member, User 

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize the database
db.init_app(app)  # Initialize db with the app
migrate = Migrate(app, db)

# Create the database and tables
with app.app_context():
    db.create_all()


# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Page to display users
@app.route('/users')
def list_users():
    users = User.query.all()  # Fetch all users from the database
    return render_template('users.html', users=users)

# Route to handle user registration
@app.route('/users', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Create a new User instance
        new_user = User(username=username, password=password, role=role)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('User added successfully!', 'success')
        return redirect(url_for('list_users'))  # Redirect to the user list

    return render_template('add_user.html')

@app.route('/delete_user/<username>', methods=['GET'])
def delete_user(username):
    global users
    # Filter out the user with the matching username
    users = [user for user in users if user['username'] != username]
    flash('User deleted successfully!')
    return redirect(url_for('list_users'))

@app.route('/edit_user/<username>', methods=['GET'])
def edit_user(username):
    # Find the user to edit
    user = next((u for u in users if u['username'] == username), None)
    if user is None:
        flash('User not found.')
        return redirect(url_for('list_users'))
    return render_template('edit_user.html', user=user)

@app.route('/update_user/<username>', methods=['POST'])
def update_user(username):
    global users
    password = request.form['password']
    role = request.form['role']
    
    # Find the user and update their details
    for user in users:
        if user['username'] == username:
            user['password'] = password
            user['role'] = role
            break

    flash('User updated successfully!')
    return redirect(url_for('list_users'))

@app.route('/members')
def list_members():
    members = Member.query.all()  # Fetch all members from the database
    return render_template('members.html', members=members)

@app.route('/membership', methods=['GET', 'POST'])
def membership():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
       # gender= request.form['gender']
        phoneNo = request.form['phoneNo']
        height = request.form['height']
        weight = request.form['weight']
        emergency_contact = request.form['emergency_contact']
        address = request.form['address']
        membership_package = request.form['membership_package']
        
        # Create a new Member instance and add it to the database
        new_member = Member(
            name=name,
            email=email,
            #gender=gender,
            age=age,
            phoneNo=phoneNo,
            height=height,
            weight=weight,
            emergency_contact=emergency_contact,
            address=address,
            membership_package=membership_package
        )
        
        db.session.add(new_member)
        db.session.commit()  # Save to the database

        flash('Member added successfully!', 'success')
        return redirect(url_for('list_members'))  # Redirect to member list page

    return render_template('add_member.html')

# Route to add a new member
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        age = request.form['age']
        phoneNo = request.form['phoneNo']
        height = request.form['height']
        weight = request.form['weight']
        emergency_contact = request.form['emergency_contact']
        address = request.form['address']
        membership_package = request.form['membership_package']

        # Create a new Member instance
        new_member = Member(
            name=name,
            email=email,
            gender=gender,
            age=age,
            phoneNo=phoneNo,
            height=height,
            weight=weight,
            emergency_contact=emergency_contact,
            address=address,
            membership_package=membership_package
        )

        db.session.add(new_member)
        db.session.commit()

        flash('Member added successfully!', 'success')
        return redirect(url_for('list_members'))  # Redirect to the member list

    return render_template('add_member.html')


if __name__ == "__main__":
    app.run(debug=True) 