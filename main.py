import customtkinter as ctk
from login_page import LoginPage
from main_page import MainPage
from baselayout import BaseLayout
from partner_page import PartnerPage


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Optigrün")
        self.set_window_size(250, 300)

        self.auth_manager = None
        self._frame = None
        self.switch_frame(LoginPage)

    def switch_frame(self, frame_class, width=None, height=None):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(expand=True, fill="both")

        # Set window size if width and height are provided
        if width is not None and height is not None:
            self.set_window_size(width, height)

    def set_window_size(self, width, height):
        self.geometry(f"{width}x{height}+{self.get_center_x(width)}+{self.get_center_y(height)}")

    def get_center_x(self, width):
        screen_width = self.winfo_screenwidth()
        return (screen_width - width) // 2

    def get_center_y(self, height):
        screen_height = self.winfo_screenheight()
        return (screen_height - height) // 2
