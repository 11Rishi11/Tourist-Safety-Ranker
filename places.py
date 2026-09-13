"""
places.py
---------
Top attractions per city.

Only cities we've actually researched have real attraction lists.
Everything else returns an empty list + a flag so the frontend can
honestly show "Coming soon" instead of fabricated places.
"""

ATTRACTIONS = {
    'Kolkata': ['Victoria Memorial', 'Howrah Bridge', 'Indian Museum', 'Dakshineswar Kali Temple', 'Park Street'],
    'Chennai': ['Marina Beach', 'Kapaleeshwarar Temple', 'Fort St. George', 'San Thome Basilica', 'Government Museum'],
    'Pune': ['Shaniwar Wada', 'Aga Khan Palace', 'Sinhagad Fort', 'Dagdusheth Halwai Ganpati Temple', 'Pataleshwar Cave Temple'],
    'Hyderabad': ['Charminar', 'Golconda Fort', 'Hussain Sagar Lake', 'Ramoji Film City', 'Chowmahalla Palace'],
    'Bengaluru': ['Lalbagh Botanical Garden', 'Bangalore Palace', 'Cubbon Park', 'ISKCON Temple', 'Vidhana Soudha'],
    'Ahmedabad': ['Sabarmati Ashram', 'Adalaj Stepwell', 'Jama Masjid', 'Kankaria Lake', 'Sidi Saiyyed Mosque'],
    'Mumbai': ['Gateway of India', 'Marine Drive', 'Elephanta Caves', 'Chhatrapati Shivaji Terminus', 'Juhu Beach'],
    'Kochi': ['Fort Kochi Beach', 'Chinese Fishing Nets', 'Mattancherry Palace', 'Jew Town & Synagogue', 'Marine Drive Kochi'],
    'Jaipur': ['Hawa Mahal', 'Amber Fort', 'City Palace', 'Jantar Mantar', 'Nahargarh Fort'],
    'Delhi': ['Red Fort', 'India Gate', 'Qutub Minar', "Humayun's Tomb", 'Lotus Temple'],
}


def get_places_for_city(city_name):
    """
    Returns (places_list, has_real_data: bool)
    has_real_data=False means we don't have verified attraction data yet —
    the frontend should show a "Coming soon" state instead of an empty list
    that looks like a bug.
    """
    places = ATTRACTIONS.get(city_name)
    if places:
        return places, True
    return [], False