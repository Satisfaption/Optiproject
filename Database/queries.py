from datetime import datetime
from functools import lru_cache
from typing import Dict, Any, Optional
from pymongo.errors import PyMongoError
from bson import ObjectId
import logging
from Database.exceptions import QueryError

logger = logging.getLogger(__name__)


class DatabaseQueries:
    def __init__(self, db):
        self.db = db

    @lru_cache(maxsize=128)
    def get_table_data(self, query_hash: str, collection_name: str) -> Dict:
        """Get table data with caching"""
        try:
            collection = self.db[collection_name]
            table_data = {}

            query = self._unhash_query(query_hash)

            partners = collection.find(query)
            partners_list = list(partners)

            for partner in partners_list:
                kundennummer = partner.get('Kundennummer')

                table_data[kundennummer] = {
                    '_id': str(partner['_id']),
                    'Name': partner.get('Name'),
                    'Straße': partner.get('Straße'),
                    'Postleitzahl': partner.get('Postleitzahl'),
                    'Ort': partner.get('Ort'),
                    'Gebietsleiter': partner.get('Gebietsleiter'),
                    'Präferierter DD': partner.get('Präferierter DD'),
                    'Pisa': partner.get('Pisa'),
                    'Zusatzinfo': partner.get('Zusatzinfo'),
                    'Begrünungsart': partner.get('Begrünungsart', {}),
                    'Latitude': partner.get('Latitude'),
                    'Longitude': partner.get('Longitude')
                }

            return table_data

        except PyMongoError as e:
            raise QueryError(f"Failed to fetch table data: {e}")

    @staticmethod
    def build_partner_query(begruenungsart: str, flaeche: int) -> Dict[str, Any]:
        """MongoDB query for search"""
        query = {
            f'Begrünungsart.{begruenungsart}': {'$exists': True},
            f'Begrünungsart.{begruenungsart}.Fläche (Minimum)': {'$lte': flaeche},
            f'Begrünungsart.{begruenungsart}.Fläche (Maximum)': {'$gte': flaeche}
        }

        return query

    def get_partner_by_id(self, partner_id: str, collection_name: str) -> Dict | None:
        """Get a single partner by ID"""
        try:
            try:
                partner_object_id = ObjectId(partner_id)
            except Exception:
                raise ValueError(f"Invalid partner_id: {partner_id}")

            collection = self.db[collection_name]
            partner = collection.find_one({"_id": ObjectId(partner_object_id)})
            if partner:
                # Convert ObjectId to string
                partner_data = {
                    '_id': str(partner['_id']),
                    'Name': str(partner.get('Name', '')),
                    'Pisa': str(partner.get('Pisa', '')),
                    'Straße': str(partner.get('Straße', '')),
                    'Postleitzahl': str(partner.get('Postleitzahl', '')),
                    'Ort': str(partner.get('Ort', '')),
                    'Gebietsleiter': str(partner.get('Gebietsleiter', '')),
                    'Kundennummer': str(partner.get('Kundennummer', '')),
                    'Zusatzinfo': str(partner.get('Zusatzinfo', '')),
                    'Begrünungsart': partner.get('Begrünungsart', {}),
                    'Latitude': partner.get('Latitude'),
                    'Longitude': partner.get('Longitude')
                }
                return partner_data
            return None

        except PyMongoError as e:
            raise QueryError(f"Failed to fetch partner: {e}")

    def update_partner(self, partner_id: str, partner_data: Dict[str, Any], collection_name: str) -> None:
        """Update an existing partner"""
        try:
            collection = self.db[collection_name]

            update_data = partner_data.copy()
            update_data.pop('_id', None)

            collection.update_one(
                {"_id": ObjectId(partner_id)},  # Convert string ID to ObjectId
                {"$set": update_data}
            )

            self.get_table_data.cache_clear()

        except PyMongoError as e:
            raise QueryError(f"Failed to update partner: {e}")

    def insert_partner(self, partner_data: Dict[str, Any], collection_name: str) -> str:
        """Insert a new partner"""
        try:
            collection = self.db[collection_name]

            if not partner_data.get('Name'):
                raise QueryError("Name darf nicht leer sein.")

            partner_data.pop('_id', None)

            result = collection.insert_one(partner_data)

            self.get_table_data.cache_clear()

            return str(result.inserted_id)

        except PyMongoError as e:
            raise QueryError(f"Failed to insert partner: {e}")

    def delete_partner(self, partner_id: str, collection_name: str) -> None:
        """Delete a partner"""
        try:
            collection = self.db[collection_name]

            result = collection.delete_one({"_id": ObjectId(partner_id)})

            if result.deleted_count == 0:
                raise QueryError(f"No partner found with ID: {partner_id}")

            self.get_table_data.cache_clear()

        except PyMongoError as e:
            raise QueryError(f"Failed to delete partner: {e}")

    @staticmethod
    def _hash_query(query: Dict[str, Any]) -> str:
        """Convert query dict to string for caching"""
        return str(dict(sorted(query.items())))

    @staticmethod
    def _unhash_query(query_hash: str) -> Dict[str, Any]:
        """Convert hashed query back to dict"""
        try:
            query_str = query_hash.strip("'")
            import ast
            return ast.literal_eval(query_str)
        except Exception:
            return {}

    def create_database_user(self, username: str, password: str, roles: list) -> None:
        """Create a new user"""
        try:
            self.db.command("createUser", username, pwd=password, roles=roles)
        except PyMongoError as e:
            raise QueryError(f"Failed to create user: {e}")

    def update_database_user(self, username: str, password: str, roles: list) -> None:
        """Update an existing user"""
        try:
            self.db.command("updateUser", username, pwd=password, roles=roles)
        except PyMongoError as e:
            raise QueryError(f"Failed to update user: {e}")

    def delete_database_user(self, username: str) -> None:
        """Delete an existing user"""
        try:
            self.db.command("dropUser", username)
        except PyMongoError as e:
            raise QueryError(f"Failed to delete user: {e}")

    def save_ors_count(self, count):
        """Save ORS usage count"""
        try:
            self.db.get_collection("Änderungsprotokoll").update_one(
                {"timestamp": datetime.now().date().isoformat()},
                {
                    "$set": {"type": "ors"},
                    "$inc": {"ors_usage_count": count}
                },
                upsert=True
            )
        except Exception as e:
            print(f"Error saving ORS usage count: {e}")

    def get_latest_ors_count(self):
        """Retrieve latest ORS usage count"""
        try:
            latest_entry = self.db.get_collection("Änderungsprotokoll").find_one(
                {"timestamp": datetime.now().date().isoformat()},
                sort=[("timestamp", -1)]
            )
            if latest_entry and "ors_usage_count" in latest_entry:
                return latest_entry["ors_usage_count"]
            return 0
        except Exception as e:
            print(f"Error retrieving ORS usage count: {e}")
            return 0
