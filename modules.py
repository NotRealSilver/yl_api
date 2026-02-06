import requests
import math
from io import BytesIO


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitiude = math.radians(a_lat + b_lat) / 2
    lat_lon_factor = math.cos(radians_lattitiude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx ** 2 + dy ** 2)

    return distance


def search_maps(text, **kwargs):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": text,
        "lang": "ru_RU",
        "type": "biz"
    }
    search_params.update(kwargs)

    response = requests.get(search_api_server, params=search_params)
    if not response:
        return
    json_response = response.json()

    return json_response


def geocode(geocode, **kwargs):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": geocode,
        "format": "json"
    }
    geocoder_params.update(kwargs)

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        raise Exception(response.status_code)

    json_response = response.json()
    return json_response['response']['GeoObjectCollection']['featureMember'][0]


def get_spn_from_geoobject(gobj):
    envelope = gobj['GeoObject']['boundedBy']['Envelope']
    ld_lon, ld_lat = map(float, envelope['lowerCorner'].split())
    ru_lon, ru_lat = map(float, envelope['upperCorner'].split())
    return ru_lon - ld_lon, ru_lat - ld_lat


def company_info(data):
    return data['features'][0]["properties"]["CompanyMetaData"]


def company_coords(data):
    return data['features'][0]['geometry']['coordinates']


def feature_geometry(feature):
    return feature["geometry"]


def get_geoobject_coord(g):
    coord = tuple(map(float, g['GeoObject']['Point']['pos'].split()))
    return coord


def static_maps(ll=None, **kwargs):
    map_params = {
        "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
    }
    if ll:
        map_params["ll"] = ll
    map_params.update(kwargs)

    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    if not response:
        raise Exception(response.status_code)
    return BytesIO(response.content)
