import tkinter as tk
from user_management import UserManger

#Create a instance for the UserManager
user_manager = UserManger()

def register_user():
    username = entry_username.get()
    password = entry_password.get()
    role = role_var.get()

    result = user_manager.register_user(username,password,role)
    print(result)   

def login_user():
    username = entry_username.get()
    password = entry_password.get()
    user = user_manager.authenticate_user(username,password)

    if user:
        print(f"Welcome {user.role} {username}!!!!")
    else:
        print("Login Failed !!!!.")


def create_main_window():
    #Create the main window
    root = tk.Tk()
    root.title("GYM MANAGEMENT SYSTEM")
    root.geometry("400x300")

    #Add a label and button
    label = tk.Label(root, text="Welcome to Divine Tribe Gym Management System", font=("Arial",16))
    label.pack(pady=20)

#Username And Password inputs
    #Username    
    tk.Label(root, text="Username:").pack()
    global entry_username
    entry_username = tk.Entry(root)
    entry_username.pack(pady=5)
    #Password
    tk.Label(root, text="Password:").pack()
    global entry_password
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=5)

    #Role Selection
    global role_var
    role_var = tk.StringVar(value="Admin")
    tk.Label(root,text="Select Role:").pack()
    tk.Radiobutton(root, text="Admin", variable=role_var, value="Admin").pack()
    tk.Radiobutton(root, text="Trainer", variable=role_var, value="Trainer").pack()
    tk.Radiobutton(root, text="Finance", variable=role_var, value="Finance").pack()

    #Buttons
    tk.Button(root, text="Register", command=register_user).pack(pady=10)
    tk.Button(root, text="Login", command=login_user).pack(pady=10)
    
    def sign_in_user():
        """Sign in an exisiting user."""
        username = entry_username.get()
        message = user_manager.sign_in_user(username)
        print(message)
    
    def sign_out_user():
        """Sign out an exisiting User."""
        username = entry_username.get()
        message = user_manager.sign_out_user(username)
        print(message)

    def show_membership_status():
        """Show membership status of a user"""
        username = entry_username.get()
        status = user_manager.get_memebership_status(username)
        print(status)

    #add Button in the create_main_window function
    tk.Button(root, text="Sign In!", command=sign_in_user).pack(pady=10)
    tk.Button(root, text="Sign Out!", command=sign_out_user).pack(pady=10)    
    tk.Button(root, text="Membership Status!", command=show_membership_status).pack(pady=10)   
    root.mainloop()

if __name__ == "__main__":
    create_main_window()