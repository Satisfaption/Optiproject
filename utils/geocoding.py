import time
import os
import requests

from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2
from utils.env_loader import EnvVars
from functools import lru_cache


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

@lru_cache(maxsize=1000)
def get_coordinates_cached(address: str) -> tuple:
    """Geocoding using Nominatim with caching

    Args:
        address (str): Full address to geocode.

    Returns:
        tuple: (latitude, longitude) or (None, None) if not found.
    """
    user_agent = os.getenv(EnvVars.USER_AGENT)
    geolocator = Nominatim(user_agent=user_agent)

    time.sleep(1)  # Rate-limit: 1 request per second

    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Geocoding error for address '{address}': {e}")

    return None, None

def get_coordinates(plz: str, street: str = None, town: str = None) -> tuple:
    """Build address for Nominatim

    Args:
        plz (str): Postal code.
        street (str, optional): Street name.
        town (str, optional): Town name.

    Returns:
        tuple: (latitude, longitude) or (None, None) if not found.
    """
    address_parts = []
    if street:
        address_parts.append(street)
    address_parts.append(str(plz))
    if town:
        address_parts.append(town)
    address_parts.append("Germany")  # country for better accuracy

    address = ", ".join(address_parts)
    return get_coordinates_cached(address)

def calculate_driving_distance(start_lat, start_lon, end_lat, end_lon):
    """Calculate driving distance between two points using OpenRouteService API

    Args:
        start_lat (float): Latitude of the starting point
        start_lon (float): Longitude of the starting point
        end_lat (float): Latitude of the destination
        end_lon (float): Longitude of the destination

    Returns:
        Tuple of (Distance, Error)
        Distance: Distance in meters (float), or None if failed
        Error: HTTPError Code, or None if failed
    """
    api_key = os.getenv(EnvVars.ORS_API_KEY)
    ORS = os.getenv(EnvVars.ORS_API_KEY)
    if not api_key:
        raise RuntimeError("OpenRouteService API key not found. Please check your environment configuration.")
    #url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_lon},{start_lat}&end={end_lon},{end_lat}'
    url = f'{ORS}start={start_lon},{start_lat}&end={end_lon},{end_lat}'
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if 'features' in data and data['features']:
                distance = data['features'][0]['properties']['segments'][0]['distance']
                return distance, None  # Return distance and (no) error message
            else:
                return None, response.status_code  #"No distance data returned from the server."

        except requests.exceptions.ConnectionError:
            return None, 503
        except Exception as e:
            return None, getattr(e.response, 'status_code', None) if isinstance(e, requests.exceptions.HTTPError) else None

    return None, "Unknown error occurred."