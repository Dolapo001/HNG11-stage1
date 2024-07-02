import requests
from django.http import JsonResponse
from django.views import View
import os
from dotenv import load_dotenv

load_dotenv()


def get_location_from_ip(ip_address):
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json/')
        response.raise_for_status()
        data = response.json()
        location = data.get('loc', '0,0')
        lat, lon = location.split(',')
        return lat, lon
    except requests.exceptions.RequestException as e:
        return '0', '0'


class HelloAPI(View):
    def get(self, request):
        visitor_name = request.GET.get('visitor_name', 'Visitor')
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()
        else:
            client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        lat, lon = get_location_from_ip(client_ip)
        weather_api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"

        response = requests.get(weather_url)
        weather_data = response.json()

        main_weather = weather_data.get('main')
        temp = main_weather.get('temp')

        greeting = f"Hello, {visitor_name}!, the temperature is {temp} degrees Celsius in {lat, lon}"

        return JsonResponse({
            "client_ip": client_ip,
            "location": f"{lat}, {lon}",
            "greeting": greeting
        })
