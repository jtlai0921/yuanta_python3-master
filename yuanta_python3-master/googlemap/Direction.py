import requests
from bs4 import BeautifulSoup
import googlemap.Polyline_decoder as decoder

headers = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

key = 'AIzaSyDrv1qkw-VzNS8_Xcc58vqZBZiuJaWWn6c'
origin = '台灣台北市中山區南京東路三段225號'
destination = '台北火車站'
#url = 'https://maps.googleapis.com/maps/api/geocode/json?address=台灣台北市中山區南京東路三段225號&key=your_key'
url = 'https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&key=%s' % (origin, destination, key)
html = requests.get(url, headers=headers)

print(html.text)

print(decoder.decode_polyline('s}{wC}~ydV?j@?`A?N?H?HAP?V?f@IxABdB?PMhAA~BAfC?z@EbC?|CAfE'))


