import sys
from io import BytesIO
import requests
from PIL import Image


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

organizations = json_response["features"][:10]

orgs_coordinates = []
point_data = []
for org in organizations:
    orgs_coordinates += [org["geometry"]["coordinates"]]
    if 'Hours' in org['properties']["CompanyMetaData"]:
        if 'TwentyFourHours' in org['properties']["CompanyMetaData"]['Hours']['Availabilities'][0]:
            point_data += ['pm2dgm']
        elif 'Intervals' in org['properties']["CompanyMetaData"]['Hours']['Availabilities'][0]:
            point_data += ['pm2blm']
    else:
        point_data += ['pm2grm']

pt_params = ''
for i in range(len(orgs_coordinates)):
    if i != len(orgs_coordinates) - 1:
        pt_params += ",".join([str(orgs_coordinates[i][0]), str(orgs_coordinates[i][1]), point_data[i]]) + '~'
    else:
        pt_params += ",".join([str(orgs_coordinates[i][0]), str(orgs_coordinates[i][1]), point_data[i]])

if not pt_params:
    print('Аптеки не найдены')
    sys.exit(1)

map_params = {
    "pt": pt_params,
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
