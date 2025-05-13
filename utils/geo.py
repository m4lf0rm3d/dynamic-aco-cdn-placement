from math import radians, cos, sin, asin, sqrt
import random

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def adjust_usage_based_on_time(cities):
    """
    Adjusts UsagePerHour based on the assumption:
    - It's daytime in Pakistan and nighttime in the US.
    - Western countries should have low usage (≤ 500).
    - Eastern countries should have high usage (≥ 5000).
    
    Args:
        cities: List of city dictionaries (must have 'long' and 'UsagePerHour')
        
    Returns:
        Modified list of cities with adjusted UsagePerHour
    """
    for city in cities:
        longitude = float(city['long'])

        # Western countries: longitudes roughly from -180 to 0
        if longitude > 0:
            city['UsagePerHour'] = random.randint(50, 200)  # Random low usage
        # Eastern countries: longitudes from 0 to 180
        else:
            city['UsagePerHour'] = random.randint(1000, 5000)  # Random high usage
    
    return cities
