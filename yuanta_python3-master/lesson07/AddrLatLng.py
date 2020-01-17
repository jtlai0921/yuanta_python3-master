import requests
from bs4 import BeautifulSoup
import lesson07.Polyline_decoder as decoder

headers = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

key = 'AIzaSyC33pWa8pjCkNWuAtLfUx3MxfRG4ye3Zs0'
url = 'https://maps.googleapis.com/maps/api/geocode/json?address=台灣台北市中山區南京東路三段225號&key=%s' % key
print(url)
html = requests.get(url, headers=headers)

print(html.text)


