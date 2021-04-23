import wikipedia as wk
import json

from django.shortcuts import render
from urllib.request import urlopen
from django.views.decorators.csrf import csrf_exempt
from ipware import get_client_ip
from django.conf import settings

API_KEY = settings.API_KEY
API_IP_KEY = settings.API_IP_KEY


#  function to find user's IP location, by default return user IP
#       'ip' - represents, that it's user's IP address
def find_ip_address(ip=''):
    try:
        response1 = urlopen("http://ipwhois.app/json/" + ip)
        response2 = urlopen("http://ip-api.com/json/" + ip)
        response3 = urlopen("http://api.ipapi.com/" + ip + "?access_key=" + API_IP_KEY)

        # return JSON with details about IP address
        return [json.load(response1), json.load(response2), json.load(response3)]
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
        return f'https://www.google.com/maps/embed/v1/place?key={API_KEY}&q={lat},{lng}&maptype=satellite&zoom=18'
    except:
        return f'https://www.google.com/maps/embed/v1/place?key={API_KEY}&q='


# some services give different results for ip, but in my research `ip-api` gives more correct results,
# so we will check whether the services give the same result:
#   if so -  we give data from `ipwhois`
#   if not (but same country) - we combine data from `ip-api` and `ipwhois`
#   if they issued different countries - then we issue data from `ip-api`
def analyze_api(data_apis):
    keys1_replace = ['city', 'region', 'latitude', 'longitude', 'org', 'timezone']
    keys2_replace = ['city', 'regionName', 'lat', 'lon', 'isp', 'timezone']

    if (data_apis[0]['country'] == data_apis[1]['country'] and data_apis[0]['city'] == data_apis[1]['city']) \
            or (data_apis[0]['country'] == data_apis[2]['country_name'] and data_apis[0]['city'] == data_apis[2]['city']):
        # check equality of lng, lat from API1 and API3
        if int(float(data_apis[0]['latitude'])) == int(data_apis[2]['latitude']) \
                and int(float(data_apis[0]['longitude'])) == int(data_apis[2]['longitude']):
            data_apis[0]['latitude'] = data_apis[2]['latitude']
            data_apis[0]['longitude'] = data_apis[2]['longitude']
            return data_apis[0]
        else:
            return data_apis[0]
    elif int(float(data_apis[0]['latitude'])) == int(data_apis[2]['latitude']) \
                and int(float(data_apis[0]['longitude'])) == int(data_apis[2]['longitude']):
        data_apis[0]['latitude'] = data_apis[2]['latitude']
        data_apis[0]['longitude'] = data_apis[2]['longitude']
        return data_apis[0]
    elif data_apis[0]['country'] == data_apis[1]['country']:
        data = data_apis[1]

        for i in range(len(keys1_replace)):
            data[keys1_replace[i]] = data_apis[1][keys2_replace[i]]

        data['country_flag'] = data_apis[0]['country_flag']
        return data
    else:
        data = data_apis[1]
        data['latitude'] = data.pop('lat')
        data['longitude'] = data.pop('lon')
        data['country_flag'] = 'https://imgur.com/a/SClnaQB'

        return data


# function to render template's html and data
@csrf_exempt
def index(request):
    if 'ip_address' in request.GET:  # fetching IP address from template
        data = find_ip_address(request.GET['ip_address'])  # if user enters data than it'll find it's IP details
        data = analyze_api(data)
    else:
        client_ip, is_routable = get_client_ip(request)
        if client_ip is None:
            # Unable to get the client's IP address
            data = find_ip_address('8.8.8.8')  # return standard IP address
            data = analyze_api(data)
        else:
            # We got the client's IP address
            if is_routable:
                # The client's IP address is publicly routable on the Internet
                data = find_ip_address(client_ip)  # return user IP address
                data = analyze_api(data)
            else:
                # The client's IP address is private
                data = find_ip_address('8.8.8.8')  # return standard IP address
                data = analyze_api(data)
    try:
        # try to fetch URL for MAP using lat, lng fetched from IP
        map_url = get_map_url(data['latitude'], data['longitude'])
        page_link = get_url(f"{data['city']} in {data['country']}")  # fetching wikipedia page link
    except:
        map_url = f'https://www.maps.google.com'
        page_link = 'https://www.wikipedia.org'

    return render(request, "ip_locator/ip-locator.html",
                  {'data': data, 'page_link': page_link, 'map_url': map_url})
