import logging
from datetime import datetime

class Logger:
    def __init__(self, db):
        self.db = db
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.ensure_collection_exists("Änderungsprotokoll")

    def ensure_collection_exists(self, collection_name):
        """Check if the collection exists and create it if it does not"""
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name).create_index("timestamp", expireAfterSeconds=2592000)  # 30 days
            self.logger.info(f"Collection '{collection_name}' created.")

    def log_user_action(self, user, action, target):
        """user logs format"""
        log_entry = {
            "timestamp": datetime.now(),
            "user": user,
            "action": action,
            "target": target,
            "type": "user"  # identifier for user actions
        }
        self.db.get_collection("Änderungsprotokoll").insert_one(log_entry)
        self.logger.info(f"{user} hat {target} {action} um {log_entry['timestamp']}")

    def log_partner_action(self, user, action, target):
        """partner logs format"""
        log_entry = {
            "timestamp": datetime.now(),
            "user": user,
            "action": action,
            "target": target,
            "type": "partner"  # identifier for partner actions
        }
        self.db.get_collection("Änderungsprotokoll").insert_one(log_entry)
        self.logger.info(f"{user} hat {target} {action} um {log_entry['timestamp']}")