import time
import os
from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2
import requests
from utils.env_loader import EnvVars

OPENROUTE_API_KEY = os.getenv(EnvVars.ORS_API_KEY)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate Haversine distance"""
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

def get_coordinates(plz: str, street: str = None, town: str = None) -> tuple:
    """Get coordinates from address information"""
    time.sleep(1)  # Nominatim rate limit of 1 call per sec

    address_parts = []
    if street:
        address_parts.append(street)
    address_parts.append(str(plz))
    if town:
        address_parts.append(town)
    address_parts.append("Germany")  # Add country for better accuracy

    address = ", ".join(address_parts)

    geolocator = Nominatim(user_agent="my_geocoder")
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Geocoding error: {e}")

    return None, None

def calculate_driving_distance(start_lat, start_lon, end_lat, end_lon):
    """
    Calculate driving distance between two points using OpenRouteService API.

    Args:
        start_lat (float): Latitude of the starting point.
        start_lon (float): Longitude of the starting point.
        end_lat (float): Latitude of the destination.
        end_lon (float): Longitude of the destination.

    Returns:
        float: Distance in meters, or None if failed.
    """
    api_key = OPENROUTE_API_KEY
    url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_lon},{start_lat}&end={end_lon},{end_lat}'
    #url = f'{ORS}start={start_lon},{start_lat}&end={end_lon},{end_lat}'
    max_retries = 3
    retry_delay = 0.5

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if 'features' in data and data['features']:
                distance = data['features'][0]['properties']['segments'][0]['distance']
                return distance
            else:
                return None
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 503 and attempt < max_retries - 1:
                print(
                    f"503 error occurred, retrying in {retry_delay} seconds... (attempt {attempt + 1} of {max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2
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

    return None