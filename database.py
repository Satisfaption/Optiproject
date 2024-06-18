from urllib.parse import quote_plus
import bcrypt
from pymongo import MongoClient, errors
import re


class Database:
    _instances = {}
    current_user = None
    current_user_uri = None

    def __new__(cls, uri, dbname):
        if uri not in cls._instances:
            instance = super(Database, cls).__new__(cls)
            cls._instances[uri] = instance
            instance.__initialized = False
        return cls._instances[uri]

    def __init__(self, uri, dbname):
        self.guest_client = None
        if self.__initialized:
            return
        self.__initialized = True
        self.uri = uri
        self.dbname = dbname
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        self.client = self.get_mongo_client(self.uri)
        if self.client:
            self.db = self.client[self.dbname]
        else:
            raise ConnectionError("Failed to connect to the MongoDB server.")

    def get_mongo_client(self, uri, timeout=60000):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=timeout)
            client.server_info()  # Trigger a server selection to check connection
            print("Connected to MongoDB server.")
            return client
        except (
                errors.ServerSelectionTimeoutError,
                errors.ConnectionFailure,
                errors.ConfigurationError,
                errors.PyMongoError) as err:
            print(f"MongoDB connection error: {err}")
            return None

    def save_customer(self, customer_data):
        if self.db is None:
            raise ConnectionError("No database connection.")
        collection = self.db['Partner']
        # Using an upsert operation to insert a new customer or update an existing one
        collection.update_one(
            {"Kundennummer": customer_data.get("Kundennummer")},
            {"$set": customer_data},
            upsert=True
        )

    def get_matching_names(self, pattern):
        if self.db is None:
            raise ConnectionError("No database connection.")
        partners = self.db['Partner']
        regex_pattern = f'.*{re.escape(pattern)}.*'
        return [partner['Name'] for partner in partners.find({'Name': {'$regex': regex_pattern, '$options': 'i'}})]

    def get_table_data(self, query):
        if self.db is None:
            raise ConnectionError("No database connection.")
        partner_collection = self.db['Partner']
        table_data = {}

        # Query partners based on query input dict
        partners = partner_collection.find(query)

        # Extract relevant data and store it in a dictionary
        for partner in partners:
            kundennummer = partner['Kundennummer']
            name = partner['Name']
            street = partner['Straße']
            plz = partner['Postleitzahl']
            ort = partner['Ort']

            table_data[kundennummer] = {
                'Name': name,
                'Straße': street,
                'Postleitzahl': plz,
                'Ort': ort
            }

        return table_data

    def delete_data(self, kundennummer):
        if self.db is None:
            raise ConnectionError("No database connection.")
        collection = self.db['Partner']
        return collection.delete_many({"Kundennummer": {"$in": kundennummer}})

    def find_partner(self, query):
        db = self.db['Partner']
        partner = db.find_one(query)
        return partner

    def close_connection(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None


""" Example use case for later
admin_db = Database(uri=ADMIN_MONGODB_URI, dbname=MONGODB_NAME)
admin_db.save_customer(customer_data)
"""
