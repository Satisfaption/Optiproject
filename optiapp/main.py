import customtkinter as ctk
from login_page import LoginPage
from update import prompt_update


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title("Optigrün")

        self.auth_manager = None
        self._frame = None
        self.after(100, self.check_updates)

    def check_updates(self):
        prompt_update(self, self.on_no_update, self.on_yes_update)

    def on_no_update(self):
        self.switch_frame(LoginPage, width=250, height=300)
        self.deiconify()

    def on_yes_update(self):
        pass

    def switch_frame(self, frame_class, width=None, height=None):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(expand=True, fill="both")

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
