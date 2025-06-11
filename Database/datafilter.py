from utils.geocoding import get_coordinates, calculate_distance, calculate_driving_distance
from Database.queries import DatabaseQueries


class DataFilter:
    def __init__(self, db_queries: DatabaseQueries):
        self.db_queries = db_queries
        self.ors_usage_count = 0

    def filter_data(self, plz, flaeche, begruenungsart, partner_type, street=None, town=None):
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
            coordinates = get_coordinates(plz, street, town)

        filtered_data = {}
        errors_4xx = {}
        error_messages = []

        # Filter by distance if coordinates are available
        for kundennummer, details in table_data.items():
            try:
                # Get the maximum allowed distance
                greening_details = details['Begrünungsart'].get(begruenungsart, {})
                max_distance = greening_details.get('Entfernung')

                if not max_distance:
                    #print(f"No max distance for {kundennummer}, skipping.")
                    continue

                try:
                    max_distance = float(max_distance)
                except (ValueError, TypeError) as e:
                    #print(f"Invalid max distance for {kundennummer}: {max_distance}, skipping.")
                    continue

                # Get partner coordinates
                partner_lat = details.get('Latitude')
                partner_long = details.get('Longitude')

                if not all([coordinates, partner_lat, partner_long]):
                    #print(f"Missing coordinates for {kundennummer}, skipping.")
                    continue

                # Calculate straight-line distance first
                user_lat, user_lon = coordinates
                haversine_distance = calculate_distance(user_lat, user_lon, partner_lat, partner_long)
                #print(f"Haversine distance for {kundennummer}: {haversine_distance} km")

                # If straight-line distance exceeds max, skip
                if haversine_distance > max_distance:
                    #print(f"Haversine distance {haversine_distance} > {max_distance} for {kundennummer}, skipping.")
                    continue

                # If distance is 0 (same location) or very small, use it directly
                if haversine_distance < 0.1:
                    distance_km = haversine_distance
                else:
                    road_distance, status_code = calculate_driving_distance(user_lat, user_lon, partner_lat, partner_long)
                    self.db_queries.save_ors_count()
                    if road_distance:
                        distance_km = round(road_distance / 1000, 2)
                        #print(f"Road distance for {kundennummer}: {distance_km} km")
                    else:
                        if status_code and 400 <= status_code <= 500:
                            errors_4xx[kundennummer] = f"Error {status_code}"
                            continue
                        elif status_code and status_code > 500:
                            error_messages.append(f'{status_code}: Server ist nicht erreichbar oder nicht online.')
                            return None, error_messages
                        else:
                            #print(f"Unknown error or no data for {kundennummer}, skipping.")
                            continue

                # Check if distance is within limit
                if distance_km > max_distance:
                    #print(f"Distance {distance_km} > {max_distance} for {kundennummer}, skipping.")
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

            except Exception as e:
                #print(f"Error processing {kundennummer}: {e}")
                continue

        if errors_4xx:
            error_messages.append(f"Fehler für diese Einträge: {errors_4xx}")

        return filtered_data, error_messages