import os
from Database.connection import Database
from Database.exceptions import DatabaseConnectionError, AuthenticationError, DatabaseError
from utils.env_loader import EnvVars
from urllib.parse import quote_plus
import logging


logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self):
        self.dbname = os.getenv(EnvVars.DB_NAME)
        self.uri_template = os.getenv(EnvVars.URI_TEMPLATE)
        self.current_user = None
        self.db_instance = None

    def authenticate_user(self, username, password):
        """Authenticate as user"""
        if not username or not password:
            return False, "Benutzername und Passwort werden benötigt."

        try:
            encoded_username = quote_plus(username)
            encoded_password = quote_plus(password)
            uri = self.uri_template.format(username=encoded_username, password=encoded_password)

            self.db_instance = Database(uri, self.dbname)
            self.current_user = username
            return True, "Login bestätigt."

        except AuthenticationError:
            return False, "Benutzername oder Passwort falsch."

        except DatabaseConnectionError:
            raise DatabaseError(
                "Verbindung zur Datenbank fehlgeschlagen.\n"
                "Bitte überprüfen Sie Ihre Internetverbindung."
            )

        except Exception:
            return False, "Ein unerwarteter Fehler ist aufgetreten. Bitte versuchen Sie es später erneut."

    def authenticate_guest(self):
        """Authenticate as guest user"""
        try:
            guest_uri = os.getenv('MONGODB_URI_GUEST')
            if not guest_uri:
                return False, "Gast-Login ist nicht konfiguriert."

            self.db_instance = Database(guest_uri, self.dbname)
            self.current_user = "Guest"
            return True, "Login erfolgreich."

        except DatabaseConnectionError:
            raise DatabaseError(
                "Verbindung zur Datenbank fehlgeschlagen.\n"
                "Bitte überprüfen Sie Ihre Internetverbindung."
            )

        except AuthenticationError:
            raise DatabaseError(
                "Gast-Login ist derzeit nicht möglich.\n"
                "Bitte versuchen Sie es später erneut."
            )

        except Exception as e:
            raise DatabaseError(f"Unerwarteter Fehler beim Gast-Login: {str(e)}")

    def get_db(self):
        if not self.db_instance:
            raise DatabaseConnectionError("Keine aktive Datenbankverbindung.")
        return self.db_instance

    def get_current_user(self):
        return self.current_user

    def logout(self):
        try:
            if self.db_instance:
                self.db_instance.close_connection()
                self.db_instance = None
            self.current_user = None
        except Exception:
            raise DatabaseError("Fehler beim Logout.")