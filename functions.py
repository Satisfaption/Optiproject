import os
import sys
import time

from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2
import requests
from pymongo import MongoClient
from config import MONGODB_URI_GUEST
from pymongo.errors import ServerSelectionTimeoutError


def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in kilometers
    return distance


def get_coordinates(street, plz, town):
    if street is None:
        street = ''
    address = f"{street}, {plz}, {town}"

    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address)

    if location:
        return location.latitude, location.longitude
    else:
        return None, None


def update_coordinates(street, plz, town, result_label):
    lat, lon = get_coordinates(street, plz, town)
    if lat is not None and lon is not None:
        result_label.config(text=f"Latitude: {lat}\nLongitude: {lon}")
    else:
        result_label.config(text="Address not found")


def calculate_driving_distance(start_lat, start_lon, end_lat, end_lon):
    api_key = '5b3ce3597851110001cf62489a6945fd9904480090dc413078afb8b2'  # Replace with your API key
    url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_lon},{start_lat}&end={end_lon},{end_lat}'
    response = requests.get(url)
    data = response.json()
    if 'features' in data and data['features']:
        distance = data['features'][0]['properties']['segments'][0]['distance']
        duration = data['features'][0]['properties']['segments'][0]['duration']
        return distance, duration
    else:
        return None, None


def get_table_data(street, plz, town, selected_greening, perimeter):
    # Calculate user's coordinates
    user_lat, user_lon = get_coordinates(street, plz, town)

    client = get_mongo_client(MONGODB_URI_GUEST)
    db = client['Optigrün']
    partners_collection = db['Partner']

    table_data = {}

    # Query partners that offer the selected greening type
    partners = partners_collection.find({f'Begrünungsart.{selected_greening}': {'$exists': True}})

    for partner in partners:
        kundennummer = partner['Kundennummer']
        name = partner['Name']
        pisa = partner['Pisa']
        plz = partner['Postleitzahl']
        ort = partner['Ort']
        partner_lat = partner['Latitude']
        partner_long = partner['Longitude']
        begruenungsart_data = partner['Begrünungsart']

        # Check if the selected greening type is available for this partner
        if selected_greening in begruenungsart_data:
            details = begruenungsart_data[selected_greening]
            flache_min = details['Fläche (Minimum)']
            flache_max = details['Fläche (Maximum)']
            # entfernung = details['Entfernung']

            # Calculate the haversine distance
            haversine_distance = calculate_distance(user_lat, user_lon, partner_lat, partner_long)
            if haversine_distance <= perimeter:
                print(f"{name} im Ort {ort} liegt mit {haversine_distance} im Umkreis.")
                distance_road, _ = calculate_driving_distance(user_lat, user_lon, partner_lat, partner_long)
                if distance_road is not None:
                    distance_km = distance_road / 1000
                    distance_km = round(distance_km, 2)
                    if kundennummer not in table_data:
                        table_data[kundennummer] = {
                            'Name': name,
                            'Pisa': pisa,
                            'PLZ': plz,
                            'Ort': ort,
                            'Distances': {}
                        }

                    table_data[kundennummer]['Distances'][selected_greening] = {
                        'Fläche (Minimum)': flache_min,
                        'Fläche (Maximum)': flache_max,
                        'Distance_km': distance_km
                    }

    client.close()
    return table_data


def get_mongo_client(uri, retries=5, delay=5):
    for i in range(retries):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=50000)
            # Attempt an operation to check if the connection is successful
            client.admin.command('ping')
            return client
        except ServerSelectionTimeoutError as err:
            print(f"Attempt {i + 1}/{retries} failed: {err}")
            time.sleep(delay)
    raise Exception("Failed to connect to MongoDB after multiple retries.")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # noinspection PyUnresolvedReferences
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except Exception:
        base_path = os.path.abspath(".")

    # Adjust for _internal directory if present
    if os.path.exists(os.path.join(base_path, '_internal')):
        base_path = os.path.join(base_path, '_internal')

    return os.path.join(base_path, relative_path)