from geopy.geocoders import Nominatim

def get_locations(address_list):
    geolocator = Nominatim(user_agent="my_app")
    locations = []
    for address in address_list:
        location = geolocator.geocode(address)
        locations.append(location)
    return locations

my_location_list = [
    "os. Bohaterów Września, Kraków, Poland",
    "os. Kolorowe, Kraków, Poland",
    "Przemysłowa 4, Kraków, Poland"
]

location_list = get_locations(my_location_list)
for location in location_list:
    print(location.address, location.latitude, location.longitude)

