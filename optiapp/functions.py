import os
import sys
import time
from dotenv import load_dotenv

from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2
import requests
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

load_dotenv()
MONGODB_URI_GUEST = os.getenv('MONGODB_URI_GUEST')
OPENROUTE_API_KEY = os.getenv('OPENROUTE_API_KEY')
ORS = os.getenv('ORS')


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
    time.sleep(1)
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
    api_key = OPENROUTE_API_KEY  # Replace with your API key
    url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_lon},{start_lat}&end={end_lon},{end_lat}'
    #url = f'{ORS}start={start_lon},{start_lat}&end={end_lon},{end_lat}'
    max_retries = 3
    retry_delay = 0.5  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            data = response.json()

            if 'features' in data and data['features']:
                distance = data['features'][0]['properties']['segments'][0]['distance']
                duration = data['features'][0]['properties']['segments'][0]['duration']
                return distance, duration
            else:
                return None, None
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 503 and attempt < max_retries - 1:
                print(
                    f"503 error occurred, retrying in {retry_delay} seconds... (attempt {attempt + 1} of {max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"HTTP error occurred: {http_err}")
                break
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            break
        except ValueError as json_err:
            print(f"JSON decode error occurred: {json_err}")
            print("Response content:", response.text)
            break

    return None, None


def get_filtered_data(street, plz, town, flaeche, table_data, greening_selection):
    # Calculate user's coordinates
    user_lat, user_lon = get_coordinates(street, plz, town)

    filtered_data = {}

    for kundennummer, details in table_data.items():
        name = details['Name']
        pisa = details['Pisa']
        ort = details['Ort']
        zipcode = details['Postleitzahl']
        gebietsleiter = details['Gebietsleiter']
        partner_lat = details['Latitude']
        partner_long = details['Longitude']
        begruenungsart_data = details['Begrünungsart']
        area_matches = True  # assumption of true

        if greening_selection not in begruenungsart_data:
            continue

        greening_details = begruenungsart_data[greening_selection]

        if flaeche is not None:
            area_matches = False
            flaeche_min = greening_details.get('Fläche (Minimum)')
            flaeche_max = greening_details.get('Fläche (Maximum)')
            if flaeche_min is not None and flaeche_max is not None:
                try:
                    flaeche_min = float(flaeche_min)
                    flaeche_max = float(flaeche_max)
                    if flaeche_min <= flaeche <= flaeche_max:
                        area_matches = True
                except ValueError:
                    continue  # Skip to the next item if area values are invalid

        if not area_matches:
            continue  # Skip distance calculation if area does not match

            # Proceed with distance calculations only if area check is passed or area filter is not used
        entfernung = greening_details.get('Entfernung')
        if entfernung is not None:
            entfernung = float(entfernung)

            # Calculate the haversine distance
            haversine_distance = calculate_distance(user_lat, user_lon, partner_lat, partner_long)

            if haversine_distance <= entfernung:
                distance_road, _ = calculate_driving_distance(user_lat, user_lon, partner_lat, partner_long)
                if distance_road is not None:
                    distance_km = distance_road / 1000
                    distance_km = round(distance_km, 2)
                    if distance_km <= entfernung:
                        if kundennummer not in filtered_data:
                            filtered_data[kundennummer] = {
                                'Name': name,
                                'Pisa': pisa,
                                'Gebietsleiter': gebietsleiter,
                                'Postleitzahl': zipcode,
                                'Ort': ort,
                                'Distances': {}
                            }
                        filtered_data[kundennummer]['Distances'][greening_selection] = {
                            'Fläche (Minimum)': greening_details['Fläche (Minimum)'],
                            'Fläche (Maximum)': greening_details['Fläche (Maximum)'],
                            'Distance_km': distance_km
                        }

    return filtered_data


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
    """ Get the absolute path to a resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)