from pymongo import MongoClient, errors
from urllib.parse import quote_plus
from config import MONGODB_URI_TEMPLATE, MONGODB_URI_GUEST, MONGODB_NAME


class AuthManager:
    def __init__(self):
        self.dbname = MONGODB_NAME
        self.uri_template = MONGODB_URI_TEMPLATE
        self.current_user = None
        self.current_user_uri = None

    def authenticate_user(self, username, password):
        encoded_username = quote_plus(username)
        encoded_password = quote_plus(password)
        uri = self.uri_template.format(username=encoded_username, password=encoded_password)

        try:
            client = MongoClient(uri)
            client.list_database_names()  # Verify connection
            self.current_user = username
            self.current_user_uri = uri
            return True
        except errors.OperationFailure:
            return False

    def authenticate_guest(self):
        try:
            client = MongoClient(MONGODB_URI_GUEST)
            client.list_database_names()  # Verify connection
            self.current_user = 'Guest'
            self.current_user_uri = MONGODB_URI_GUEST
            return True
        except errors.OperationFailure:
            return False

    def get_current_user_uri(self):
        return self.current_user_uri

    def get_current_user(self):
        return self.current_user
