import sys

from pymongo import MongoClient, errors
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os


def load_environment():
    # Determine the directory where the executable is running from
    extDataDir = os.getcwd()
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        extDataDir = sys._MEIPASS

    # Construct the path to the .env file
    dotenv_path = os.path.join(extDataDir, '.env')

    # Load environment variables from the .env file
    load_dotenv(dotenv_path=dotenv_path)


# Call the function to load environment variables
load_environment()
MONGODB_URI_TEMPLATE = os.getenv('MONGODB_URI_TEMPLATE')
MONGODB_URI_GUEST = os.getenv('MONGODB_URI_GUEST')
MONGODB_NAME = os.getenv('MONGODB_NAME')


class AuthManager:
    def __init__(self):
        self.dbname = MONGODB_NAME
        self.uri_template = MONGODB_URI_TEMPLATE
        self.current_user = None
        self.current_user_uri = None

    def authenticate_user(self, username, password):
        if not username or not password:
            return False, "Benutzername und Password werden benötigt."
        encoded_username = quote_plus(username)
        encoded_password = quote_plus(password)
        uri = self.uri_template.format(username=encoded_username, password=encoded_password)

        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=2000)
            client.list_database_names()  # Verify connection
            self.current_user = username
            self.current_user_uri = uri
            return True, "Authenticated successfully."
        except errors.OperationFailure:
            return False, "Ungültiger Benutzername oder Passwort."
        except errors.ConnectionFailure:
            return False, "Verbindung zur Datenbank fehlgeschlagen."

    def authenticate_guest(self):
        try:
            client = MongoClient(MONGODB_URI_GUEST, serverSelectionTimeoutMS=2000)
            client.list_database_names()  # Verify connection
            self.current_user = 'Guest'
            self.current_user_uri = MONGODB_URI_GUEST
            return True, "Authenticated successfully."
        except errors.OperationFailure:
            return False, "Fehlerhafter Gast-Login."
        except errors.ConnectionFailure:
            return False, "Verbindung zur Datenbank fehlgeschlagen."

    def get_current_user_uri(self):
        return self.current_user_uri

    def get_current_user(self):
        return self.current_user