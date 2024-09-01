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
        self.username_entry.bind("<Return>", self.on_enter)
        self.password_entry.bind("<Return>", self.on_enter)

        self.guest_button = ctk.CTkButton(self, text="Gastzugang", command=self.login_guest)
        self.guest_button.grid(row=4, column=0, columnspan=2, pady=10)

    def go_to_main_page(self):
        from main_page import MainPage
        self.master.switch_frame(MainPage, 1400, 700)

    def on_enter(self, event):
        self.login_user()

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        auth_manager = AuthManager()
        success, message = auth_manager.authenticate_user(username, password)

        if success:
            # Navigate to the main application page
            self.master.auth_manager = auth_manager
            self.go_to_main_page()
        else:
            # Show an error message using ErrorPopup
            self.show_warning(message)

    def login_guest(self):
        auth_manager = AuthManager()
        success, message = auth_manager.authenticate_guest()

        if success:
            # Navigate to the main application page
            self.master.auth_manager = auth_manager
            self.go_to_main_page()
        else:
            # Show an error message using ErrorPopup
            self.show_warning(message)

    def show_warning(self, message):
        warning_popup = ctk.CTkToplevel(self)
        warning_popup.title("Warnung")

        # Center the popup on the screen
        window_width = 300
        window_height = 120
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        warning_popup.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        # Make the popup modal and always on top
        warning_popup.transient(self)
        warning_popup.grab_set()

        warning_label = ctk.CTkLabel(warning_popup, text=message, wraplength=250)
        warning_label.pack(padx=20, pady=20)

        ok_button = ctk.CTkButton(warning_popup, text="OK", command=warning_popup.destroy)
        ok_button.pack(pady=(0, 10))

        # Ensure the popup is closed properly
        warning_popup.protocol("WM_DELETE_WINDOW", warning_popup.destroy)
