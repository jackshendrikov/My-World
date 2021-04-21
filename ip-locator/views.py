from django.shortcuts import render
import geocoder
import wikipedia as wk
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

API_KEY = settings.API_KEY


#  function to find user's IP location
#       'ip' - represents, that it's user's IP address
def find_ip_address(ip='ip'):
    try:
        # return JSON with details about IP address
        return (geocoder.ip(ip)).json
    except:
        return find_ip_address()  # send details about user's address only


# function to create a link to Wikipedia by keyword
def get_url(keyword):
    links = wk.search(keyword)  # search keyword in Wiki
    page = wk.page(links[0])  # take 1st result
    return page.url


# function for generating a Map URL to be embedded in a website.
#   lat - latitude
#   lng - longitude
def get_map_url(lat, lng):
    try:
        return f'https://www.google.com/maps/embed/v1/place?key={API_KEY}&q={lat},{lng}'
    except:
        return f'https://www.google.com/maps/embed/v1/place?key={API_KEY}&q='
