import requests
from django.http import JsonResponse
import os
from dotenv import load_dotenv

load_dotenv()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_location_data(ip_address):
    response = requests.get(f'https://ipinfo.io/{ip_address}/json/').json()
    city = response.get('city')
    lat = response.get("latitude", 0)
    lon = response.get("longitude", 0)
    return city, lat, lon


def get_weather_data(lat, lon):
    weather_api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    weather_url = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric")
    weather_data = weather_url.json()
    main_weather = weather_data.get('main', {})
    temp = main_weather.get('temp', 273.15)
    return temp - 273.15


def greeting(request):
    visitor_name = request.GET.get('visitor_name', 'guest')
    ip_address = get_client_ip(request)
    city, lat, lon = get_location_data(ip_address)
    temp_celsius = get_weather_data(lat, lon)

    return JsonResponse({
        "client_ip": ip_address,
        "location": city,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temp_celsius:.2f} degrees Celsius in {city}"
    })

