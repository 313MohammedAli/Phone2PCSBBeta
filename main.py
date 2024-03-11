from multiprocessing import Process, Manager
from tkinter import messagebox, Tk
import authentication
import customtkinter as ctk

def run_server(q):
    import server
    server.main(q)

def run_gui(q):
    import gui
    gui.main(q)

class LoginWindow:
    def __init__(self, q):
        self.q = q
        self.root = ctk.CTk()
        self.root.title("Login")
        self.root.geometry("300x200")

        # Username field
        ctk.CTkLabel(self.root, text="Username:").pack(pady=(20, 0))
        self.entry_username = ctk.CTkEntry(self.root)
        self.entry_username.pack(pady=(0, 20))

        # Password field
        ctk.CTkLabel(self.root, text="Password:").pack()
        self.entry_password = ctk.CTkEntry(self.root, show="*")
        self.entry_password.pack(pady=(0, 20))

        # Login button
        login_button = ctk.CTkButton(self.root, text="Login", command=self.attempt_login)
        login_button.pack()

    def attempt_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        auth_response = authentication.authenticate_user(username, password)

        if auth_response is not None and 'AuthenticationResult' in auth_response:
            messagebox.showinfo("Login Success", "You are now logged in.", parent=self.root)
            self.q.put("authenticated")  # Pass successful authentication message to queue
            self.root.destroy()  # Close login window
        else:
            messagebox.showerror("Login failed", "Invalid username or password", parent=self.root)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    with Manager() as manager:
        q = manager.Queue()

        # Show login window first and wait for successful authentication
        login_app = LoginWindow(q)
        login_app.run()

        if not q.empty() and q.get() == "authenticated":
            # Start server and GUI processes after successful authentication
            server_process = Process(target=run_server, args=(q,))
            gui_process = Process(target=run_gui, args=(q,))

            server_process.start()
            gui_process.start()

            server_process.join()
            gui_process.join()
