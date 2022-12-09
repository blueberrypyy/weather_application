import requests
from datetime import datetime as dt
import time as t

data = [{'name': 'Boulder', 'local_names': {'zh': '博尔德/波德', 'en': 'Boulder', 'ja': 'ボールダー'}, 'lat': 40.0154155, 'lon': -105.270241, 'country': 'US', 'state': 'Colorado'}] 
word = 'api.openweathermap.org/data/2.5/forecast?lat={0}&lon={1}&appid=faa30bca64456bb8655bdda8f22865c3'

geocode_url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&limit=&appid=faa30bca64456bb8655bdda8f22865c3'
hourly_url = 'http://api.openweathermap.org/data/2.5/forecast?lat={0}&lon={1}&appid=faa30bca64456bb8655bdda8f22865c3&units=imperial'

# Determine lat/lon for hourly url 
city_geo = requests.get(geocode_url.format('Denver')).json()
lat = city_geo[0]['lat']
lon = city_geo[0]['lon']

city_hourly = requests.get(hourly_url.format(lat, lon)).json()
#print('CITY HOURLY: ', city_hourly)


def time_converter(x):
    current = t.strptime(x, '%H:%M:%S')
    return current.strftime('%I:%M %p')

def timeStamp():
    now = t.time()
    local = t.localtime(now)
    return t.strftime('%I:%M %p', local)

def dateStamp():
    year = dt.now().year 
    month = dt.now().strftime('%B').title()
    day = dt.now().strftime('%A')
    day_num = dt.now().strftime('%d')
    return [year, month, day, day_num]

print(dateStamp())




'''
count = 0
for item in city_hourly['list']:
    count += 1

    #weather_time = item['dt_txt'].split()[1] 
    #print(time_converter(weather_time))
    print(item['dt_txt'].split()[0][5:].replace('-', '/'))

    #print(item['weather'][0]['description'])
    #print(item['main']['temp'])

    print('\n')
    if count > 9:
        break
'''
