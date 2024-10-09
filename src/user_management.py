class User:
    """Base Calls for all the users."""
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, username, password):
        #Placeholder for login logic
        return self.username == username and self.password == password


class Admin(User):
    """Admin role with full access"""
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role = "Admin"

    def access_membership_page(self):
        return "Accessing membership page with full permissions"

class Trainer(User):
    """Trainer with limited access"""
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role = "Trainer"
    
    def access_membership_page(self):
        return "Accessing membership page with limited permissions"
    
class Finance(User):
    """Finance with limited access"""
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role = "Finance"
    
    def access_membership_page(self):
        return "Accessing membership page with limited permissions"
    
class UserManger:
    """Class to manage all the users."""
    def __init__(self):
        self.users = [] # store registerd Users
        self.memberships = {}

    def register_user(self, username, password, role):
        """Regisster a New user"""
        if role == "Admin":
            user = Admin(username,password)
        elif role == "Trainer":
            user = Trainer(username,password)
        elif role == "Finance":
            user = Finance(username,password)
        else: 
            raise ValueError("Invalid Role Specified")
        
        self.users.append(user)

        self.memberships[username] = Membership(username, membership_type)
        return f"{role} '{username}' Registered Successfully! with {membership_type} membership!!!"
    
    def authenticate_user(self, username, password):
        for user in self.users:
            if user.login(username, password):
                return user
        return None

    def sign_in_user(self, username):
        """Sign in the user"""
        if username in self.memberships:
            return self.memberships[username].sign_in()
        return "User not found"

    def sign_out_user(self,username):
        """Sign out the user"""
        if username in self.memberships:
            return self.memberships[username].sign_out()
        return "User not found"
    
    def get_memebership_status(self, username):
        """Get the membership status."""
        if username in self.memberships:
            return self.memberships[username].status()
        return "User Not found."
