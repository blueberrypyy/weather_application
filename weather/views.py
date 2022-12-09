from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
import requests
from environs import Env
from .models import City, Words
from .forms import CityForm

import time as t
from datetime import datetime as dt 

class AboutPageView(TemplateView): 
    template_name = 'about.html'

   

env = Env()
env.read_env()
WEATHER_API_KEY = env.str('WEATHER_API_KEY')

# Date and month function
def dateStamp():
    year = dt.now().year 
    month = dt.now().strftime('%B').title()
    day = dt.now().strftime('%A')
    day_num = dt.now().strftime('%d')
    return [year, month, day_num, day]



# Timestamp function
def timeStamp():
    now = t.time()
    local = t.localtime(now)
    return t.strftime('%I:%M %p', local)


def time_converter(x):
    current = dt.strptime(x, '%H:%M:%S')
    return current.strftime('%I:%M %p')


#def city_detail(request)
def delete_word(request, word_id):
    word = Words.objects.get(pk=word_id)
    word.delete()
    return redirect('word_page')

def word_view(request):
    words = Words.objects.all()
    return render(request, 'weather/front_end_test.html', {})

def search_city(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        cities = City.objects.filter(name__contains=searched)
        return render(request, 'weather/searched_city.html', {'searched': searched, 'cities': cities})

    else:
        return render(request, 'weather/searched_city.html', {})



def delete_city(request, city_id):
    city = City.objects.get(pk=city_id)
    city.delete()
    return redirect('home')
 

#city = 'New York'
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=faa30bca64456bb8655bdda8f22865c3'
    #print(cities)
    weather_data = []
    timestamp = timeStamp()
    datestamp = dateStamp()

    if request.user.is_authenticated:
        current_user = request.user.id
        cities = City.objects.filter(account=current_user)

        # Date and time stuff
        #month_name = dt.now().strftime('%B')
        #month_number = list(calendar.month_name).index(month)
        #month_number = int(month_number)
        # Get current year 
        #now = datetime.now()
        #current_year = now.year
        # Create calendar
        #cal = HTMLCalendar().formatmonth(year, month_number)

        # Add city form 
        if request.method == 'POST': # only true if form is submitted
            form = CityForm(request.POST) # add actual request data to form for processing
            if form.is_valid():
                city_form = form.save(commit=False)
                city_form.account = request.user.id
                city_form.save() # will validate and save if validated
        form = CityForm()

        for city in cities:
            city_weather = requests.get(url.format(city.name)).json() # request the API data and convert the JSON to Python data types

            weather = {
                    'city': city,
                    'temperature': city_weather['main']['temp'],
                    'description': city_weather['weather'][0]['description'],
                    'icon': city_weather['weather'][0]['icon'],
                    }
            weather_data.append(weather) # add the data of the current city to our list

        context = {'weather_data': weather_data, 'form': form, 'timestamp': timestamp, 'datestamp': datestamp}
        return render(request, 'weather/index.html', context) # returns the index template

    else:
        return render(request, 'weather/index.html', {})


def info_city(request, city_id):
    city = City.objects.get(pk=city_id)
    #print('\nCITY:', city)
    timestamp = timeStamp()
    print(timestamp)

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=faa30bca64456bb8655bdda8f22865c3'
    geocode_url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&limit=&appid=faa30bca64456bb8655bdda8f22865c3'
    hourly_url = 'http://api.openweathermap.org/data/2.5/forecast?lat={0}&lon={1}&appid=faa30bca64456bb8655bdda8f22865c3&units=imperial'
    #maps_url = 'https://tile.openweathermap.org/map/precipitation_new/3/2/5.png?appid=faa30bca64456bb8655bdda8f22865c3'

    # Determine lat/lon for hourly url 
    city_geo = requests.get(geocode_url.format(city.name)).json()
    lat = city_geo[0]['lat']
    lon = city_geo[0]['lon']
    #print('\nCITY GEO: ', city_geo, '\n')
    #print('\nLAT:', city_geo[0]['lat'], 'LON:', city_geo[0]['lon'])


    hourly_weather_list = []
    city_hourly = requests.get(hourly_url.format(lat, lon)).json()
    for item in city_hourly['list']:
        #print('\n', item)
        hourly_weather_data = {
                'hourly_date': item['dt_txt'].split()[0][5:].replace('-', '/'),
                'hourly_time': time_converter(item['dt_txt'].split()[1]),
                'hourly_description': item['weather'][0]['description'],
                'hourly_icon': item['weather'][0]['icon'],

                'hourly_temperature': item['main']['temp'],
                'hourly_min': item['main']['temp_min'],
                'hourly_max': item['main']['temp_max'],
                'hourly_feels_like': item['main']['feels_like'],
                'hourly_humidity': item['main']['humidity'],
                'hourly_precipitation': str(int(float(item['pop'] * 100))),
                'hourly_wind': item['wind']['speed'],
                'hourly_gust': item['wind']['gust'],
                

                }

        hourly_weather_list.append(hourly_weather_data)

        #hourly_weather_time = time_converter(item['dt_text'].split()[1])
        #print('CITY HOURLY: ', city_hourly)
            
    city_weather = requests.get(url.format(city.name)).json() # request the API data and convert the JSON to Python data types
    #print('CITY_WEATHER:', city_weather)

    #city_weather_map = requests.get(maps_url)
    #print('\n WEATHER MAP:', city_weather_map)

    weather = {
            # Original parameters
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],


            # Detailed parameters
            'temp_min': city_weather['main']['temp_min'],
            'temp_max': city_weather['main']['temp_max'],
            'temp_feels_like': city_weather['main']['feels_like'],
            'humidity': city_weather['main']['humidity'],
            'wind': city_weather['wind']['speed'],
            'timestamp': timestamp,

            # Hourly parameters
            'hourly_weather_list': hourly_weather_list,


            }
    #print('WEATHER:', weather)

    context = {'weather': weather}
    return render(request, 'weather/info_city.html', context) # returns the index template



#DEBUG
#url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=faa30bca64456bb8655bdda8f22865c3'
#city = 'Denver'
#city_weather = requests.get(url.format(city)).json() # request the API data and convert the JSON to Python data types
#print(city_weather)
#print('\n', city_weather['main']['temp'])




