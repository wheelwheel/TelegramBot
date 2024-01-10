from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_email@myserver.com")

location = geolocator.reverse("23.45137,120.46500")

print(location.raw['address']['county'])
print(location.raw['address']['town'])