from utils.geocoding import get_coordinates, calculate_distance, calculate_driving_distance
from Database.queries import DatabaseQueries


class DataFilter:
    def __init__(self, db_queries: DatabaseQueries):
        self.db_queries = db_queries
        self.ors_usage_count = 0

    def filter_data(self, plz, flaeche, begruenungsart, partner_type="Partner", street=None, town=None):
        """Filter data based on user input
        flaeche = (minimum) area that a company performs their work
        begruenungsart = 3 different variations of work done
        partner_type = collection (mongoDB 'table') of partnered companies
        street, town and plz = address data"""
        # only return data where begruenungsart and flaeche match
        query = self.db_queries.build_partner_query(begruenungsart=begruenungsart, flaeche=int(float(flaeche)))
        query_hash = self.db_queries._hash_query(query)
        table_data = self.db_queries.get_table_data(query_hash, collection_name=partner_type)

        coordinates = None
        if plz:
            address_parts = []
            if street:
                address_parts.append(street)
            address_parts.append(plz)
            if town:
                address_parts.append(town)

            # calculate coordinates for entered address
            coordinates = get_coordinates(" ".join(address_parts))

        filtered_data = {}

        # Filter by distance if coordinates are available
        for kundennummer, details in table_data.items():
            try:
                # Get the maximum allowed distance
                greening_details = details['Begrünungsart'].get(begruenungsart, {})
                max_distance = greening_details.get('Entfernung')

                if not max_distance:
                    continue

                try:
                    max_distance = float(max_distance)
                except (ValueError, TypeError) as e:
                    continue

                # Get partner coordinates
                partner_lat = details.get('Latitude')
                partner_long = details.get('Longitude')

                if not all([coordinates, partner_lat, partner_long]):
                    continue

                # Calculate straight-line distance first
                user_lat, user_lon = coordinates
                haversine_distance = calculate_distance(user_lat, user_lon, partner_lat, partner_long)

                # If straight-line distance exceeds max, skip
                if haversine_distance > max_distance:
                    continue

                # If distance is 0 (same location) or very small, use it directly
                if haversine_distance < 0.1:
                    distance_km = haversine_distance
                else:
                    try:
                        # Try to calculate road distance
                        road_distance, _ = calculate_driving_distance(user_lat, user_lon, partner_lat, partner_long)
                        if road_distance:
                            distance_km = round(road_distance / 1000, 2)
                        else:
                            distance_km = round(haversine_distance, 2)
                    except Exception as e:
                        distance_km = round(haversine_distance, 2)

                # Check if distance is within limit
                if distance_km > max_distance:
                    continue

                filtered_data[kundennummer] = {
                    'Name': details['Name'],
                    'Straße': details['Straße'],
                    'Postleitzahl': details['Postleitzahl'],
                    'Ort': details['Ort'],
                    'Gebietsleiter': details['Gebietsleiter'],
                    'Präferierter DD': details['Präferierter DD'],
                    'Pisa': details['Pisa'],
                    'Zusatzinfo': details['Zusatzinfo'],
                    'Distance': distance_km
                }
                self.ors_usage_count += 1

            except Exception:
                continue

        self.db_queries.save_ors_count(self.ors_usage_count)

        return filtered_data