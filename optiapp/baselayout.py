import customtkinter as ctk
from PIL import Image

from functions import resource_path


class BaseLayout(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_frame = None
        self.side_frame = None
        self.footer_frame = None
        self.configure(fg_color='white')
        self.image_path = resource_path('ressources/Optigruen-Logo_335px.png')

        self.setup_logo_frame()
        self.setup_header_frame()
        self.setup_footer_frame()
        self.setup_side_frame()
        self.setup_main_frame()

        self.configure_layout()

    def setup_logo_frame(self):
        logo_frame = ctk.CTkFrame(self, border_width=4, border_color='#c8f7be', fg_color='#c8f7be')
        logo_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=3, pady=3)

        logo_frame.columnconfigure(0, weight=1)
        logo_frame.rowconfigure(0, weight=1)
        logo_frame.propagate(False)

        logo_image = ctk.CTkImage(light_image=Image.open(self.image_path), size=(180, 180))
        image_label = ctk.CTkLabel(logo_frame, image=logo_image, text='')
        image_label.grid(row=0, column=0)

    def setup_header_frame(self):
        header_frame = ctk.CTkFrame(self, border_width=4, border_color='#c8f7be', fg_color='#c8f7be')
        header_frame.grid(row=0, column=1, columnspan=5, sticky="nsew", padx=3, pady=3)
        header_frame.propagate(False)

        header_frame.columnconfigure(0, weight=10)
        header_frame.columnconfigure(1, weight=1)
        header_frame.rowconfigure(0, weight=1)

        menu_options = ["Partner", "Kunden-Suche", "Logout"]
        menu = ctk.CTkOptionMenu(header_frame, values=menu_options, command=self.handle_menu_option_select)
        menu.set("Menü")
        menu.grid(row=0, column=1)

        """partner_button = ctk.CTkButton(header_frame, text="Partner Menü", command=self.go_to_partner_page)
        partner_button.grid(row=0, column=0)
        logout_button = ctk.CTkButton(header_frame, text="Logout", command=self.go_to_login_page)
        logout_button.grid(row=0, column=1)"""

    def setup_side_frame(self):
        self.side_frame = ctk.CTkFrame(self, border_width=4, border_color='#c8f7be', fg_color='#c8f7be')
        self.side_frame.grid(row=2, column=0, rowspan=5, sticky="nsew", padx=3, pady=3)
        self.side_frame.propagate(False)

        self.side_frame.columnconfigure(0, weight=1)
        self.side_frame.rowconfigure(0, weight=1)

    def setup_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, border_width=4, border_color='#c8f7be', fg_color='#c8f7be')
        self.main_frame.grid(row=1, column=1, rowspan=5, columnspan=5, sticky="nsew", padx=3, pady=3)
        self.main_frame.propagate(False)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def setup_footer_frame(self):
        self.footer_frame = ctk.CTkFrame(self, border_width=4, border_color='#c8f7be', fg_color='#c8f7be')
        self.footer_frame.grid(row=6, column=1, columnspan=5, sticky="nsew", padx=3, pady=3)
        self.footer_frame.propagate(False)

        self.footer_frame.columnconfigure(0, weight=10)
        self.footer_frame.columnconfigure(1, weight=1)
        self.footer_frame.rowconfigure(0, weight=1)

    def configure_layout(self):
        self.rowconfigure(0, weight=1, uniform='e')
        self.rowconfigure(1, weight=1, uniform='e')
        self.rowconfigure(2, weight=5, uniform='e')
        self.rowconfigure(3, weight=5, uniform='e')
        self.rowconfigure(4, weight=5, uniform='e')
        self.rowconfigure(5, weight=5, uniform='e')
        self.rowconfigure(6, weight=5, uniform='e')
        self.columnconfigure(0, weight=1, uniform='e')
        self.columnconfigure(1, weight=1, uniform='e')
        self.columnconfigure(2, weight=1, uniform='e')
        self.columnconfigure(3, weight=1, uniform='e')
        self.columnconfigure(4, weight=1, uniform='e')
        self.columnconfigure(5, weight=1, uniform='e')

    def handle_menu_option_select(self, choice):
        command_mapping = {
            "Partner": self.go_to_partner_page,
            "Kunden-Suche": self.go_to_main_page,
            "Logout": self.go_to_login_page
        }

        command = command_mapping.get(choice)
        if command:
            command()

    def go_to_partner_page(self):
        from partner_page import PartnerPage
        self.master.switch_frame(PartnerPage, 1400, 700)

    def go_to_login_page(self):
        from login_page import LoginPage
        self.master.switch_frame(LoginPage, 250, 300)

    def go_to_main_page(self):
        from main_page import MainPage
        self.master.switch_frame(MainPage, 1400, 700)
