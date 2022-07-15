from datetime import datetime
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

# Get timezone from coordinates
tf = TimezoneFinder()
# Get lat, long from city name
geolocator = Nominatim(user_agent='xxx')

run = True
while run:
    try:
        user = input("Enter City/Country, X to exit: ")
        if user == 'x' or user == 'X':
            run = False
        else:
            city = user.capitalize()

            location = geolocator.geocode(city)

            latitude, longitude = location.latitude, location.longitude

            datez = str(tf.timezone_at(lng=longitude, lat=latitude))
            globalDate = datetime.now(pytz.timezone(datez))

            print("Timezone:", datez)
            print("Current Time is: " + globalDate.strftime('%I:%M:%S %p %Z%z'))
            print("\n")
    except:
        print("Try Again \n")
