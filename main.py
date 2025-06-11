import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from utils.env_loader import load_environment
from App_Login.login import LoginWindow
from utils.update import prompt_update, cleanup_old_version


def main():
    try:
        if not load_environment():
            QMessageBox.critical(
                None,
                "Configuration Error",
                "Konnte die Konfigurationsdatei (.env) nicht laden.\n"
                "Bitte stellen Sie sicher, dass die Datei vorhanden ist."
            )
            return 1

        app = QApplication(sys.argv)

        cleanup_old_version()
        prompt_update(None, lambda: print("User chose not to update."), on_ok_update)

        login_window = LoginWindow()
        login_window.show()

        return app.exec()

    except Exception as e:
        QMessageBox.critical(
            None,
            "Error",
            f"Fehler beim Starten der Anwendung: {str(e)}"
        )
        return 1

def on_ok_update(self):
    pass

if __name__ == "__main__":
    sys.exit(main())