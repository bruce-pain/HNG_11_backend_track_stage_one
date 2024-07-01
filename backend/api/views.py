from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpRequest
from rest_framework.decorators import api_view
import requests
import os
from pprint import pprint

def get_geodata(ip: str) -> dict[str]:
    API_KEY = os.environ.get("API_KEY")
    URL = "http://api.weatherapi.com/v1/current.json?key={}&q={}".format(API_KEY, ip)

    response = requests.get(URL).json()
    pprint(response)

    city = response["location"]["name"]
    temp = response["current"]["temp_c"]

    return {"city": city, "temp": temp}


def get_client_ip(request: HttpRequest):
    XFF: str = request.META.get("HTTP_X_FORWARDED_FOR")
    client_ip = ""

    if XFF:
        client_ip = XFF.split(',')[0]
    else:
        client_ip = request.META.get("REMOTE_ADDR")

    return client_ip

@api_view(['GET'])
def hello(request: Request):
    # get name from query
    name = request.query_params.get("visitor_name")
    # get client ip address
    client_ip = get_client_ip(request)

    # get client geodata
    geodata = get_geodata(client_ip)

    payload = {"client_ip": client_ip, "city": geodata["city"], "greeting": f"Hello, {name}!, the temperature is {geodata['temp']} degrees Celcius in {geodata['city']}"}

    return Response(data=payload)
