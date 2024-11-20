from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QApplication, QMessageBox,
                               QLineEdit, QLabel, QPushButton, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from Database.authentication import AuthManager
from Database.exceptions import DatabaseError
from Main_Window.main_window import MainWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        self.setWindowTitle("Matrix - Login")
        self.setWindowIcon(QIcon('og_transparent.ico'))
        self.setFixedSize(400, 500)

        # main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("Matrix Login")
        title.setStyleSheet("""
            QLabel {
                color: #1a1a1a;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # form layout
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(25)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Username
        username_container = QFrame()
        username_layout = QVBoxLayout(username_container)
        username_layout.setSpacing(2)
        username_layout.setContentsMargins(0, 0, 0, 0)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("")
        username_label = QLabel("Benutzername")
        self._setup_input_field(self.username_edit, username_label, is_password=False)

        username_layout.addWidget(self.username_edit)
        username_layout.addWidget(username_label)
        form_layout.addWidget(username_container)

        # Password
        password_container = QFrame()
        password_layout = QVBoxLayout(password_container)
        password_layout.setSpacing(2)
        password_layout.setContentsMargins(0, 0, 0, 0)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        password_label = QLabel("Passwort")
        self._setup_input_field(self.password_edit, password_label, is_password=True)

        password_layout.addWidget(self.password_edit)
        password_layout.addWidget(password_label)
        form_layout.addWidget(password_container)

        # Set up field references after both fields exist
        self.username_edit.other_field = self.password_edit
        self.password_edit.other_field = self.username_edit

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0066b3;
            }
            QPushButton:pressed {
                background-color: #005299;
            }
        """)
        form_layout.addWidget(self.login_button)

        # Guest login button
        self.guest_button = QPushButton("Gastzugang")
        self.guest_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.guest_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666666;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
            QPushButton:pressed {
                background-color: #e6e6e6;
            }
        """)
        form_layout.addWidget(self.guest_button)

        layout.addWidget(form_container)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
        """)

        self._init_signals()

    def _setup_input_field(self, edit: QLineEdit, label: QLabel, is_password: bool):
        """Styling for input field and its label"""
        edit.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 1px solid #cccccc;
                padding: 5px 0px;
                font-size: 14px;
                background-color: transparent;
                selection-background-color: #0078d4;
                selection-color: white;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #0078d4;
            }
        """)

        label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 12px;
                margin-top: 2px;
            }
        """)

    def _handle_focus_in(self, edit: QLineEdit, label: QLabel):
        """focus in event"""
        label.setStyleSheet("QLabel { color: #0078d4; font-size: 12px; }")
        edit.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #0078d4;
                padding: 5px 0px;
                font-size: 14px;
                background-color: transparent;
            }
        """)

        if hasattr(edit, 'other_field'):
            other_field = edit.other_field
            other_field.setStyleSheet("""
                QLineEdit {
                    border: none;
                    border-bottom: 1px solid #cccccc;
                    padding: 5px 0px;
                    font-size: 14px;
                    background-color: transparent;
                }
            """)
            if hasattr(other_field, 'my_label'):
                other_field.my_label.setStyleSheet("""
                    QLabel {
                        color: #666666;
                        font-size: 12px;
                        margin-bottom: 0px;
                    }
                """)

    def _handle_focus_out(self, edit: QLineEdit, label: QLabel):
        """focus out event"""
        if not edit.hasFocus() and not (hasattr(edit, 'other_field') and edit.other_field.hasFocus()):
            label.setStyleSheet("""
                QLabel {
                    color: #666666;
                    font-size: 12px;
                    margin-bottom: 0px;
                }
            """)
            edit.setStyleSheet("""
                QLineEdit {
                    border: none;
                    border-bottom: 1px solid #cccccc;
                    padding: 5px 0px;
                    font-size: 14px;
                    background-color: transparent;
                }
            """)

    def _handle_login(self):
        """Handle login on button click"""
        try:
            username = self.username_edit.text()
            password = self.password_edit.text()

            if not username or not password:
                QMessageBox.warning(
                    self,
                    "Login Error",
                    "Bitte geben Sie Benutzername und Passwort ein."
                )
                self.password_edit.setFocus()
                return

            self.setCursor(Qt.CursorShape.WaitCursor)
            success, message = self.auth_manager.authenticate_user(username, password)

            if success:
                self._open_main_window()
            else:
                QMessageBox.warning(self, "Login Error", message)
                self.password_edit.clear()
                self.password_edit.setFocus()

        except DatabaseError:
            QMessageBox.critical(
                self,
                "Datenbankfehler",
                "Verbindung zur Datenbank fehlgeschlagen.\n\n"
                "Bitte überprüfen Sie Ihre Internetverbindung und versuchen Sie es erneut."
            )
            self.password_edit.clear()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Ein unerwarteter Fehler ist aufgetreten:\n{str(e)}"
            )
            self.password_edit.clear()

        finally:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def _handle_guest_login(self):
        """Handle guest login attempt"""
        try:
            # Show loading state
            self.setCursor(Qt.CursorShape.WaitCursor)

            success, message = self.auth_manager.authenticate_guest()

            if success:
                self._open_main_window()
            else:
                QMessageBox.warning(
                    self,
                    "Login Error",
                    "Gast-Login fehlgeschlagen.\n\n" + message
                )

        except DatabaseError:
            QMessageBox.critical(
                self,
                "Datenbankfehler",
                "Verbindung zur Datenbank fehlgeschlagen.\n\n"
                "Bitte überprüfen Sie Ihre Internetverbindung und versuchen Sie es erneut."
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Ein unerwarteter Fehler ist aufgetreten:\n{str(e)}"
            )

    def _open_main_window(self):
        """Switch from Login to main Window on successful login"""
        if hasattr(self, 'main_window') and self.main_window.isVisible():
            self.main_window.raise_()
            return

        try:
            self.main_window = MainWindow(auth_manager=self.auth_manager)
            self.main_window.logout_signal.connect(self.show)
            self.main_window.show()
            self.hide()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Fehler beim Öffnen des Hauptfensters: {str(e)}",
                QMessageBox.StandardButton.Ok
            )

    def _init_signals(self):
        self.login_button.clicked.connect(self._handle_login)
        self.guest_button.clicked.connect(self._handle_guest_login)
        self.password_edit.returnPressed.connect(self._handle_login)
        self.username_edit.returnPressed.connect(self._handle_login)
