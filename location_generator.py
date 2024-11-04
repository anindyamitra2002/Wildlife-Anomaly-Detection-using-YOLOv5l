import random
from math import radians, sin, cos, sqrt

# Function to generate a random neighboring location within a given range
def generate_random_neighbour(lat, lon, max_distance_km):
    earth_radius_km = 6371.0

    lat_diff = max_distance_km / earth_radius_km
    lon_diff = max_distance_km / (earth_radius_km * cos(radians(lat)))

    new_lat = lat + random.uniform(-lat_diff, lat_diff)
    new_lon = lon + random.uniform(-lon_diff, lon_diff)

    return new_lat, new_lon

# Example hardcoded fixed given location
  # Maximum distance for generating random neighboring locations
def add_random_location(data, given_lat, given_lon, max_distance_km):
    for frame in data:
        for detection in frame['detections']:
            num_locations = random.randint(1, 3)  # Generate 1 to 3 random neighboring locations
            
            for _ in range(num_locations):
                new_lat, new_lon = generate_random_neighbour(given_lat, given_lon, max_distance_km)
                
                # Append new location to the detection
                detection['latitude'] = new_lat
                detection['longitude'] = new_lon

    # Print the updated data with neighboring locations
    return data
