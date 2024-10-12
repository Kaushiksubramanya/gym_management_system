from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Member
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym_management.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database
db.init_app(app)  # Initialize db with the app
migrate = Migrate(app, db)

# Create the database and tables
with app.app_context():
    db.create_all()

# User and Member models (same as before)
# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Set the route for the login page

# Route to load user from session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# **************************************************************************************************************************

# Models and other routes...

@app.route('/')
@login_required
def home():
    return render_template('dashboard.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Print the form data for debugging
        print(request.form)
        
        # Safely get the username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')

        # Ensure both fields are provided
        if not username or not password:
            flash('Username and password are required', 'danger')
            return redirect(url_for('login'))

        # Check if the user exists in the database
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)  # Log the user in
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')  # Render the login template

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        #email = request.form['email']
        
        try:
            email = request.form['email']  # Debug print statement
            print(f"Email: {email}")
        except KeyError as e:
            print(f"Error: {e}")

        
        username = request.form['username']
        password = request.form['password']
        
        # Use pbkdf2:sha256 for hashing the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        role = 'admin'  # This can be hardcoded for the first admin

        # Create and add the new admin
        new_user = User(email=email, username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Admin registered successfully!', 'success')
        return redirect(url_for('list_users'))

    return render_template('register.html')
# List Users
@app.route('/users')
@login_required
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

# Edit User (Admin only)
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)  # Fetch the user by ID
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('list_users'))

    if request.method == 'POST':
        # Update user details
        user.username = request.form['username']
        user.password = generate_password_hash(request.form['password'])  # Hash the password
        user.email = request.form['email']
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('list_users'))

    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found.', 'danger')
    return redirect(url_for('list_users'))


# Add Member
@app.route('/add_member', methods=['GET', 'POST'])
@login_required
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
        is_active = True if 'is_active' in request.form else False

        # Create a new member and add to the database
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
            membership_package=membership_package,
            is_active=is_active
        )
        db.session.add(new_member)
        db.session.commit()

        flash('Member added successfully!')
        return redirect(url_for('list_members'))

    return render_template('add_member.html')

# List Members
@app.route('/members')
@login_required
def list_members():
    members = Member.query.all()
    return render_template('members.html', members=members)

# Edit Member
@app.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    member = Member.query.get(member_id)
    if member is None:
        flash('Member not found.', 'danger')
        return redirect(url_for('list_members'))

    if request.method == 'POST':
        # Update member details
        member.name = request.form['name']
        member.email = request.form['email']
        member.gender = request.form['gender']
        member.age = request.form['age']
        member.phoneNo = request.form['phoneNo']
        member.height = request.form['height']
        member.weight = request.form['weight']
        member.emergency_contact = request.form['emergency_contact']
        member.address = request.form['address']
        member.membership_package = request.form['membership_package']
        member.is_active = True if 'is_active' in request.form else False
        
        db.session.commit()
        flash('Member updated successfully!', 'success')
        return redirect(url_for('list_members'))

    return render_template('edit_member.html', member=member)

# View a Specific member
@app.route('/view_member/<int:member_id>', methods=['GET'])
def view_member(member_id):
    member = Member.query.get(member_id)
    if member is None:
        flash('Member not found.', 'danger')
        return redirect(url_for('list_members'))

    return render_template('view_member.html', member=member)

# Delete Member
@app.route('/delete_member/<int:member_id>', methods=['POST'])
@login_required
def delete_member(member_id):
    member = Member.query.get(member_id)
    db.session.delete(member)
    db.session.commit()
    flash('Member deleted successfully!')
    return redirect(url_for('list_members'))

@app.route('/dashboard')
@login_required
def dashboard():
    total_active_users = User.query.filter_by(is_active=True).count()
    total_active_members = Member.query.filter_by(is_active=True).count()
    
    return render_template('dashboard.html', 
                           total_active_users=total_active_users, 
                           total_active_members=total_active_members)

# Initialize the app
if __name__ == '__main__':
    app.run(debug=True)











































# #**********************************************************************************************************************************************
# # Decorator to restrict access to admins
# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'role' not in session or session['role'] != 'admin':
#             flash('You do not have permission to access this page.', 'danger')
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

# @app.route('/login', methods=['POST'])
# def login():
#     print(request.method)  # This will log the method being used
#     username = request.form['username']
#     password = request.form['password']

#     user = User.query.filter_by(username=username).first()

#     if user and check_password_hash(user.password, password):
#         login_user(user)
#         flash('Login successful!')
#         return redirect(url_for('dashboard'))
#     else:
#         flash('Invalid username or password.')
#         return redirect(url_for('login'))

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html')


# # Define the logout route
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('You have been logged out', 'info')
#     return redirect(url_for('login'))

# # Home page, show different content based on role
# @app.route('/')
# def home():
#     return render_template('index.html', username=session.get('username'), role=session.get('role'))


# # Page to display users
# @app.route('/users')
# #@admin_required
# def list_users():
#     users = User.query.all()  # Fetch all users from the database
#     return render_template('users.html', users=users)

# # Route to handle user registration
# @app.route('/register', methods=['POST'])
# def register():
#     username = request.form['username']
#     password = request.form['password']
#     hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

#     new_user = User(username=username, password=hashed_password)
#     db.session.add(new_user)
#     db.session.commit()

#     flash('User registered successfully!')
#     return redirect(url_for('login'))


# @app.route('/delete_user/<username>', methods=['GET'])
# def delete_user(username):
#     global users
#     # Filter out the user with the matching username
#     users = [user for user in users if user['username'] != username]
#     flash('User deleted successfully!')
#     return redirect(url_for('list_users'))

# @app.route('/edit_user/<username>', methods=['GET'])
# def edit_user(username):
#     # Find the user to edit
#     user = next((u for u in users if u['username'] == username), None)
#     if user is None:
#         flash('User not found.')
#         return redirect(url_for('list_users'))
#     return render_template('edit_user.html', user=user)

# @app.route('/update_user/<username>', methods=['POST'])
# def update_user(username):
#     global users
#     password = request.form['password']
#     role = request.form['role']
    
#     # Find the user and update their details
#     for user in users:
#         if user['username'] == username:
#             user['password'] = password
#             user['role'] = role
#             break

#     flash('User updated successfully!')
#     return redirect(url_for('list_users'))

# @app.route('/members')
# def list_members():
#     members = Member.query.all()  # Fetch all members from the database
#     return render_template('members.html', members=members)

# @app.route('/membership', methods=['GET', 'POST'])
# #@admin_required
# def membership():
#     if request.method == 'POST':
#         # Get form data
#         name = request.form['name']
#         email = request.form['email']
#         age = request.form['age']
#        # gender= request.form['gender']
#         phoneNo = request.form['phoneNo']
#         height = request.form['height']
#         weight = request.form['weight']
#         emergency_contact = request.form['emergency_contact']
#         address = request.form['address']
#         membership_package = request.form['membership_package']
        
#         # Create a new Member instance and add it to the database
#         new_member = Member(
#             name=name,
#             email=email,
#             #gender=gender,
#             age=age,
#             phoneNo=phoneNo,
#             height=height,
#             weight=weight,
#             emergency_contact=emergency_contact,
#             address=address,
#             membership_package=membership_package
#         )
        
#         db.session.add(new_member)
#         db.session.commit()  # Save to the database

#         flash('Member added successfully!', 'success')
#         return redirect(url_for('list_members'))  # Redirect to member list page

#     return render_template('add_member.html')

# # Route to add a new member
# @app.route('/add_member', methods=['GET', 'POST'])
# def add_member():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         gender = request.form['gender']
#         age = request.form['age']
#         phoneNo = request.form['phoneNo']
#         height = request.form['height']
#         weight = request.form['weight']
#         emergency_contact = request.form['emergency_contact']
#         address = request.form['address']
#         membership_package = request.form['membership_package']

#         # Create a new Member instance
#         new_member = Member(
#             name=name,
#             email=email,
#             gender=gender,
#             age=age,
#             phoneNo=phoneNo,
#             height=height,
#             weight=weight,
#             emergency_contact=emergency_contact,
#             address=address,
#             membership_package=membership_package
#         )

#         db.session.add(new_member)
#         db.session.commit()

#         flash('Member added successfully!', 'success')
#         return redirect(url_for('list_members'))  # Redirect to the member list

#     return render_template('add_member.html')


# if __name__ == "__main__":
#     app.run(debug=True) 