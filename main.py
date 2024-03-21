import sys
from io import BytesIO
import requests
from PIL import Image
import param_tools


toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"
}

response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    print("HTTP status:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_lon, toponym_lat = toponym_coodrinates.split(" ")


search_api_server = "https://search-maps.yandex.ru/v1/"
search_params = {
    "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ",".join([toponym_lon, toponym_lat]),
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    print("HTTP status:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

json_response = response.json()

organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
org_coordinates = organization["geometry"]["coordinates"]

lls = [list(map(float, toponym_coodrinates.split())), org_coordinates]
map_params = {
    "ll": ",".join(map(str, param_tools.get_mid_ll(lls[0], lls[1]))),
    "spn": ','.join(map(str, param_tools.get_spn_tp(lls[0], lls[1]))),
    "pt": "{},{},{}~{},{},{}".format(toponym_lon, toponym_lat, 'round', 
                                     org_coordinates[0], org_coordinates[1], 'pm2dgl'),
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

if not response:
    print("HTTP status:", response.status_code, "(", response.reason, ")")
    print(response.url)
    sys.exit(1)

Image.open(BytesIO(
    response.content)).show()

distance = str(round(param_tools.lonlat_distance(map(float, toponym_coodrinates.split(" ")), org_coordinates), 2))

snippet = {
    'Расстояние':  distance + ' м',
    'Адрес': org_address,
    'Название': org_name,
    'Режим работы': organization['properties']["CompanyMetaData"]['Hours']['text']
}

for k, v in snippet.items():
    print(k, '-', v)

