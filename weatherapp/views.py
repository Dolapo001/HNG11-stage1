import requests
from django.http import JsonResponse
from django.views import View
import os
from dotenv import load_dotenv

load_dotenv()


def get_location_from_ip(ip_address):
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json/').json()
        data = response.json()
        city = data.get('city', 'Unknown')
        return city
    except Exception as e:
        print(f"Error getting location: {e}")
        return 'Unknown'


class HelloAPI(View):
    def get(self, request):
        visitor_name = request.GET.get('visitor_name', 'Visitor')
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()
        else:
            client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        city = get_location_from_ip(client_ip)
        weather_api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        weather_response = requests.get(weather_url).json()
        temperature = weather_response.get('main', {}).get('temp', 'Unknown')

        greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"

        return JsonResponse({
            "client_ip": client_ip,
            "location": city,
            "greeting": greeting
        })
