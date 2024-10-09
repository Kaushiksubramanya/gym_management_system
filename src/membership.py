class Membership:
    """Class to manage user memberships."""
    def __init__(self, username, membership_type):
        self.username = username
        self.membership_type = membership_type
        self. is_signed_in = False

    def sign_in(self):
        """Sign in the user"""
        self.is_signed_in = True
        return f"{self.username} has signed in."
    
    def sign_out(self):
        """Sign out the user"""
        self.is_signed_in = False
        return f"{self.username} has signed out."

    def status(self):
        return {
            "username" : self.username,
            "membership_type" : self.membership_type,
            "is_signed_in" : self.is_signed_in
        }