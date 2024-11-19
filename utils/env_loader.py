import os
import sys
from dotenv import load_dotenv


class EnvVars:
    URI_TEMPLATE = 'MONGODB_URI_TEMPLATE'
    URI_GUEST = 'MONGODB_URI_GUEST'
    DB_NAME = 'MONGODB_NAME'
    ORS_API_KEY = 'OPENROUTE_API_KEY'


def load_environment():
    """load env vars"""
    try:
        # Try current working directory
        env_paths = [
            os.path.join(os.getcwd(), '.env'),
            os.path.join(os.path.dirname(__file__), '..', '.env'),
        ]

        if getattr(sys, 'frozen', False):
            env_paths.append(os.path.join(sys._MEIPASS, '.env'))

        for path in env_paths:
            if os.path.exists(path):
                load_dotenv(dotenv_path=path)
                verify_environment()
                return True

        raise FileNotFoundError("Could not find .env file")

    except Exception as e:
        print(f"Error loading environment: {e}")
        return False

def verify_environment():
    """Verify"""
    uri_template = os.getenv(EnvVars.URI_TEMPLATE)
    uri_guest = os.getenv(EnvVars.URI_GUEST)
    db_name = os.getenv(EnvVars.DB_NAME)
    ors_api_key = os.getenv(EnvVars.ORS_API_KEY)

    errors = []

    if not validate_mongodb_uri(uri_guest):
        errors.append("Invalid guest URI format")
    if not validate_mongodb_uri(uri_template):
        errors.append("Invalid URI template format")
    if not db_name:
        errors.append("Missing database name")
    if not ors_api_key:
        errors.append("Missing OpenRouteService API key")

    if errors:
        raise RuntimeError("\n".join(errors))

def validate_mongodb_uri(uri: str) -> bool:
    """Validate MongoDB URI format"""
    if not uri:
        return False
    return (uri.startswith('mongodb://') or uri.startswith('mongodb+srv://')) and '@' in uri
