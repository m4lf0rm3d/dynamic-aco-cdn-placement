import csv
import random

import csv
import random

import csv
import random

def generate_city_data(path='data/cities.csv'):
    # Most populated city per country with coordinates (at least 100 entries)
    cities = [
        {"City": "Tokyo", "Country": "Japan", "lat": 35.6895, "long": 139.6917},
        {"City": "Delhi", "Country": "India", "lat": 28.7041, "long": 77.1025},
        {"City": "Shanghai", "Country": "China", "lat": 31.2304, "long": 121.4737},
        {"City": "São Paulo", "Country": "Brazil", "lat": -23.5505, "long": -46.6333},
        {"City": "Cairo", "Country": "Egypt", "lat": 30.0444, "long": 31.2357},
        {"City": "Dhaka", "Country": "Bangladesh", "lat": 23.8103, "long": 90.4125},
        {"City": "Moscow", "Country": "Russia", "lat": 55.7558, "long": 37.6173},
        {"City": "Mexico City", "Country": "Mexico", "lat": 19.4326, "long": -99.1332},
        {"City": "Istanbul", "Country": "Turkey", "lat": 41.0082, "long": 28.9784},
        {"City": "Kinshasa", "Country": "DR Congo", "lat": -4.4419, "long": 15.2663},
        {"City": "Lagos", "Country": "Nigeria", "lat": 6.5244, "long": 3.3792},
        {"City": "London", "Country": "United Kingdom", "lat": 51.5074, "long": -0.1278},
        {"City": "Bangkok", "Country": "Thailand", "lat": 13.7563, "long": 100.5018},
        {"City": "Buenos Aires", "Country": "Argentina", "lat": -34.6037, "long": -58.3816},
        {"City": "Tehran", "Country": "Iran", "lat": 35.6892, "long": 51.3890},
        {"City": "Paris", "Country": "France", "lat": 48.8566, "long": 2.3522},
        {"City": "Bogotá", "Country": "Colombia", "lat": 4.7110, "long": -74.0721},
        {"City": "Lima", "Country": "Peru", "lat": -12.0464, "long": -77.0428},
        {"City": "Jakarta", "Country": "Indonesia", "lat": -6.2088, "long": 106.8456},
        {"City": "Karachi", "Country": "Pakistan", "lat": 24.8607, "long": 67.0011},
        {"City": "Nairobi", "Country": "Kenya", "lat": -1.2921, "long": 36.8219},
        {"City": "New York City", "Country": "United States", "lat": 40.7128, "long": -74.0060},
        {"City": "Hanoi", "Country": "Vietnam", "lat": 21.0285, "long": 105.8544},
        {"City": "Berlin", "Country": "Germany", "lat": 52.5200, "long": 13.4050},
        {"City": "Madrid", "Country": "Spain", "lat": 40.4168, "long": -3.7038},
        {"City": "Kuala Lumpur", "Country": "Malaysia", "lat": 3.1390, "long": 101.6869},
        {"City": "Santiago", "Country": "Chile", "lat": -33.4489, "long": -70.6693},
        {"City": "Addis Ababa", "Country": "Ethiopia", "lat": 9.03, "long": 38.74},
        {"City": "Baghdad", "Country": "Iraq", "lat": 33.3128, "long": 44.3615},
        {"City": "Toronto", "Country": "Canada", "lat": 43.6510, "long": -79.3470},
        {"City": "Sydney", "Country": "Australia", "lat": -33.8688, "long": 151.2093},
        {"City": "Rome", "Country": "Italy", "lat": 41.9028, "long": 12.4964},
        {"City": "Seoul", "Country": "South Korea", "lat": 37.5665, "long": 126.9780},
        {"City": "Manila", "Country": "Philippines", "lat": 14.5995, "long": 120.9842},
        {"City": "Havana", "Country": "Cuba", "lat": 23.1136, "long": -82.3666},
        {"City": "Riyadh", "Country": "Saudi Arabia", "lat": 24.7136, "long": 46.6753},
        {"City": "Cape Town", "Country": "South Africa", "lat": -33.9249, "long": 18.4241},
        {"City": "Warsaw", "Country": "Poland", "lat": 52.2297, "long": 21.0122},
        {"City": "Vienna", "Country": "Austria", "lat": 48.2082, "long": 16.3738},
        {"City": "Kabul", "Country": "Afghanistan", "lat": 34.5553, "long": 69.2075},
        {"City": "Kathmandu", "Country": "Nepal", "lat": 27.7172, "long": 85.3240},
        {"City": "Doha", "Country": "Qatar", "lat": 25.276987, "long": 51.520008},
        {"City": "Singapore", "Country": "Singapore", "lat": 1.3521, "long": 103.8198},
        {"City": "Athens", "Country": "Greece", "lat": 37.9838, "long": 23.7275},
        {"City": "Oslo", "Country": "Norway", "lat": 59.9139, "long": 10.7522},
        {"City": "Stockholm", "Country": "Sweden", "lat": 59.3293, "long": 18.0686},
        {"City": "Helsinki", "Country": "Finland", "lat": 60.1695, "long": 24.9354},
        {"City": "Copenhagen", "Country": "Denmark", "lat": 55.6761, "long": 12.5683},
        {"City": "Reykjavik", "Country": "Iceland", "lat": 64.1355, "long": -21.8954},
        {"City": "Brussels", "Country": "Belgium", "lat": 50.8503, "long": 4.3517},
        {"City": "Amsterdam", "Country": "Netherlands", "lat": 52.3676, "long": 4.9041},
        {"City": "Lisbon", "Country": "Portugal", "lat": 38.7169, "long": -9.1399},
        {"City": "Prague", "Country": "Czech Republic", "lat": 50.0755, "long": 14.4378},
        {"City": "Budapest", "Country": "Hungary", "lat": 47.4979, "long": 19.0402},
        {"City": "Zurich", "Country": "Switzerland", "lat": 47.3769, "long": 8.5417},
        {"City": "Bratislava", "Country": "Slovakia", "lat": 48.1482, "long": 17.1067},
        {"City": "Ljubljana", "Country": "Slovenia", "lat": 46.0569, "long": 14.5051},
        {"City": "Sarajevo", "Country": "Bosnia and Herzegovina", "lat": 43.8486, "long": 18.3564},
        {"City": "Sofia", "Country": "Bulgaria", "lat": 42.6977, "long": 23.3219},
        {"City": "Tbilisi", "Country": "Georgia", "lat": 41.7151, "long": 44.8271},
        {"City": "Yerevan", "Country": "Armenia", "lat": 40.1792, "long": 44.4991},
        {"City": "Chisinau", "Country": "Moldova", "lat": 47.0105, "long": 28.8638},
        {"City": "Tallinn", "Country": "Estonia", "lat": 59.4372, "long": 24.7536},
        {"City": "Vilnius", "Country": "Lithuania", "lat": 54.6872, "long": 25.2797},
        {"City": "Riga", "Country": "Latvia", "lat": 56.9496, "long": 24.1052},
    ]

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['City', 'Country', 'lat', 'long', 'UsagePerHour'])
        writer.writeheader()
        for city in cities:
            usage = random.randint(100, 8000)
            writer.writerow({
                'City': city['City'],
                'Country': city['Country'],
                'lat': city['lat'],
                'long': city['long'],
                'UsagePerHour': usage
            })



def generate_server_data(path='data/edge_servers.csv'):
    # List of 30 prominent Cloudflare data center locations with approximate coordinates
    cloudflare_locations = [
        {"CDN_ID": "cdn_1", "City": "New York", "Lat": 40.7128, "Long": -74.0060},
        {"CDN_ID": "cdn_2", "City": "Los Angeles", "Lat": 34.0522, "Long": -118.2437},
        {"CDN_ID": "cdn_3", "City": "Chicago", "Lat": 41.8781, "Long": -87.6298},
        {"CDN_ID": "cdn_4", "City": "London", "Lat": 51.5074, "Long": -0.1278},
        {"CDN_ID": "cdn_5", "City": "Frankfurt", "Lat": 50.1109, "Long": 8.6821},
        {"CDN_ID": "cdn_6", "City": "Amsterdam", "Lat": 52.3676, "Long": 4.9041},
        {"CDN_ID": "cdn_7", "City": "Paris", "Lat": 48.8566, "Long": 2.3522},
        {"CDN_ID": "cdn_8", "City": "Tokyo", "Lat": 35.6895, "Long": 139.6917},
        {"CDN_ID": "cdn_9", "City": "Singapore", "Lat": 1.3521, "Long": 103.8198},
        {"CDN_ID": "cdn_10", "City": "Sydney", "Lat": -33.8688, "Long": 151.2093},
        {"CDN_ID": "cdn_11", "City": "Toronto", "Lat": 43.651070, "Long": -79.347015},
        {"CDN_ID": "cdn_12", "City": "São Paulo", "Lat": -23.5505, "Long": -46.6333},
        {"CDN_ID": "cdn_13", "City": "Johannesburg", "Lat": -26.2041, "Long": 28.0473},
        {"CDN_ID": "cdn_14", "City": "Mumbai", "Lat": 19.0760, "Long": 72.8777},
        {"CDN_ID": "cdn_15", "City": "Seoul", "Lat": 37.5665, "Long": 126.9780},
        {"CDN_ID": "cdn_16", "City": "Hong Kong", "Lat": 22.3193, "Long": 114.1694},
        {"CDN_ID": "cdn_17", "City": "Dubai", "Lat": 25.2048, "Long": 55.2708},
        {"CDN_ID": "cdn_18", "City": "Istanbul", "Lat": 41.0082, "Long": 28.9784},
        {"CDN_ID": "cdn_19", "City": "Mexico City", "Lat": 19.4326, "Long": -99.1332},
        {"CDN_ID": "cdn_20", "City": "Madrid", "Lat": 40.4168, "Long": -3.7038},
        {"CDN_ID": "cdn_21", "City": "Warsaw", "Lat": 52.2297, "Long": 21.0122},
        {"CDN_ID": "cdn_22", "City": "Vienna", "Lat": 48.2082, "Long": 16.3738},
        {"CDN_ID": "cdn_23", "City": "Brussels", "Lat": 50.8503, "Long": 4.3517},
        {"CDN_ID": "cdn_24", "City": "Copenhagen", "Lat": 55.6761, "Long": 12.5683},
        {"CDN_ID": "cdn_25", "City": "Oslo", "Lat": 59.9139, "Long": 10.7522},
        {"CDN_ID": "cdn_26", "City": "Helsinki", "Lat": 60.1695, "Long": 24.9354},
        {"CDN_ID": "cdn_27", "City": "Stockholm", "Lat": 59.3293, "Long": 18.0686},
        {"CDN_ID": "cdn_28", "City": "Lisbon", "Lat": 38.7169, "Long": -9.1399},
        {"CDN_ID": "cdn_29", "City": "Athens", "Lat": 37.9838, "Long": 23.7275},
        {"CDN_ID": "cdn_30", "City": "Bangkok", "Lat": 13.7563, "Long": 100.5018}
    ]

    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['CDN_ID', 'City', 'lat', 'long', 'CPU_Health', 'Threshold', 'Status'])
        writer.writeheader()
        for location in cloudflare_locations:
            cpu_health = round(random.uniform(30, 50), 2)
            threshold = 90
            status = "Running"
            writer.writerow({
                'CDN_ID': location['CDN_ID'],
                'City': location['City'],
                'lat': location['Lat'],
                'long': location['Long'],
                'CPU_Health': cpu_health,
                'Threshold': threshold,
                'Status': status
            })

def generate_fake_data(cities):
    """
    This function updates the `UsagePerHour` for each city in the given cities list.
    The UsagePerHour is updated with a random value between 100 and 10000.
    """
    for city in cities:
        city['UsagePerHour'] = random.randint(100, 10000)