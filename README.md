# Tailored GUI for Data Manipulation and Geo-Calculations

This project provides a **tailored GUI** that allows users to:

- **Manipulate data** efficiently for various operations.
- **Perform geo calculations** for location-based data processing.
- **Display desired output** with intuitive visualizations and user-friendly interfaces.

## Environment Variables

This project requires the following environment variables for proper configuration:

- **MONGODB_URI_TEMPLATE**: The URI template for connecting to your MongoDB instance.
- **MONGODB_URI_GUEST**: A URI for guest access to MongoDB (if applicable).
- **MONGODB_NAME**: The name of the MongoDB database to use.
- **OPENROUTE_API_KEY**: The API key for OpenRouteService to perform geospatial calculations (e.g., routing, distance calculations).

### Example .env file

```plaintext
MONGODB_URI_TEMPLATE=mongodb+srv://<user>:<password>@cluster.mongodb.net/{db_name}?retryWrites=true&w=majority
MONGODB_URI_GUEST=mongodb://localhost:27017
MONGODB_NAME=your_database
OPENROUTE_API_KEY=your_openrouteservice_api_key
