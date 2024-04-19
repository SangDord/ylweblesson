from requests import get, post, delete, put
from io import BytesIO
from PIL import Image
from pprint import pprint


response = get('http://localhost:8080/api/users_show/2')
if response.status_code != 200:
      print("HTTP status:", response.status_code, "(", response.reason, ")")
else:
      city_img = eval(response.json()['img'])
      Image.open(BytesIO(city_img)).show()