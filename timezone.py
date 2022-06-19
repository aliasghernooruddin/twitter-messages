from datetime import datetime
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

run = True
while run:
    try:
        print("Enter City/Country, X to exit")
        user = input("")
        if user == 'x' or user == 'X':
            run = False
        else:
            city = user.capitalize()
            # Get lat, long from city name
            geolocator = Nominatim(user_agent='xxx')
            location = geolocator.geocode(city)

            # Get timezone from coordinates
            tf = TimezoneFinder()
            latitude, longitude = location.latitude, location.longitude

            # Timezone
            datez = str(tf.timezone_at(lng=longitude, lat=latitude))
            globalDate = datetime.now(pytz.timezone(datez))

            print("Timezone:", datez)
            print("Current Time is:" + globalDate.strftime('%H:%M:%S %Z%z'))
            print("\n")
    except:
        print("Try Again \n")
