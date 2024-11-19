from pymongo import MongoClient, errors
from typing import Optional, Dict
import threading
import logging
from Database.exceptions import DatabaseConnectionError, AuthenticationError, DatabaseError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    _instances: Dict[str, 'Database'] = {}
    _lock = threading.Lock()

    def __init__(self, uri: str, dbname: str):
        """Initialize database connection"""
        self.uri = uri
        self.dbname = dbname
        self.client: Optional[MongoClient] = None
        self.db = None
        self.queries = None

        # Connection pool settings
        self.pool_settings = {
            'maxPoolSize': 3,  # Maximum number of connections in the pool
            'minPoolSize': 1,  # Minimum number of connections in the pool
            'maxIdleTimeMS': 30000,  # Max time a connection can be idle (30 seconds)
            'waitQueueTimeoutMS': 2000,  # How long to wait for available connection
            'serverSelectionTimeoutMS': 2000,  # How long to wait for server selection
            'retryWrites': False
        }

        self._establish_connection()

    def _establish_connection(self) -> None:
        """Connect to database"""
        try:
            self.client = MongoClient(self.uri, **self.pool_settings)
            self.client.server_info()
            self.db = self.client[self.dbname]

        except errors.OperationFailure:
            raise AuthenticationError("Ungültige Anmeldedaten")

        except errors.ServerSelectionTimeoutError:
            raise DatabaseConnectionError("Server nicht erreichbar - Bitte überprüfen Sie Ihre Internetverbindung")

        except errors.ConnectionFailure:
            raise DatabaseConnectionError("Verbindung fehlgeschlagen - Bitte überprüfen Sie Ihre Internetverbindung")

        except Exception as e:
            raise DatabaseError(f"Unerwarteter Datenbankfehler: {e}")

    def close_connection(self) -> None:
        """Close database connection"""
        if self.client:
            try:
                self.client.close()
            except Exception as e:
                logger.error(f"Error closing connection: {e}")
            finally:
                self.client = None
                self.db = None

    def is_connected(self) -> bool:
        try:
            self.client.admin.command('ping')
            return True
        except:
            return False

    def __del__(self):
        """Ensure connection is closed when object is deleted"""
        self.close_connection()

    def get_collection(self, name):
        return self.db[name]

    def update_password(self, username, new_password):
        """Updates user password"""
        if self.db is None:
            raise ConnectionError("No database connection.")

        try:
            self.db.command("updateUser", username, pwd=new_password)
            return True, "Password updated successfully."
        except errors.PyMongoError as e:
            raise Exception(f"Failed to update password: {e}")

    def load_users(self) -> list:
        """Load existing database users"""
        if self.db is None:
            raise ConnectionError("No database connection.")

        try:
            users = self.db.command("usersInfo", 1)
            user_list = [user['user'] for user in users['users']]# if user['user'] != 'Guest']
            return user_list
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen der Benutzerrollen: {str(e)}")

    def get_user_roles(self, username):
        """Get user roles"""
        try:
            user_info = self.db.command("usersInfo", username)
            roles = user_info.get('users', [{}])[0].get('roles', [])

            role_names = [role['role'] for role in roles]
            return role_names
        except Exception as e:
            logger.error(f"Error retrieving roles for user {username}: {e}")
            return []