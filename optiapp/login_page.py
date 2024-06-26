import customtkinter as ctk

from authentication import AuthManager


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(width=400, height=600)

        # configure grid layout
        self.columnconfigure(0, weight=1, uniform='e')
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='e')

        self.label = ctk.CTkLabel(self, text="Login Page")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Benutzername")
        self.username_entry.grid(row=1, column=0, padx=5)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Passwort", show="*")
        self.password_entry.grid(row=2, column=0, padx=5)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_user)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.guest_button = ctk.CTkButton(self, text="Gastzugang", command=self.login_guest)
        self.guest_button.grid(row=4, column=0, columnspan=2, pady=10)

    def go_to_main_page(self):
        from main_page import MainPage
        self.master.switch_frame(MainPage, 1400, 700)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        auth_manager = AuthManager()
        if auth_manager.authenticate_user(username, password):
            self.master.auth_manager = auth_manager
            self.go_to_main_page()
            print(f"Logged in as {auth_manager.get_current_user()}")
        else:
            print("Login failed")

    def login_guest(self):
        auth_manager = AuthManager()
        if auth_manager.authenticate_guest():
            self.master.auth_manager = auth_manager
            self.go_to_main_page()
            print(f"Logged in as {auth_manager.get_current_user()}")
        else:
            print("Guest login failed")

# to do:
# authentication
# light up entry when something is missing
