import json, urllib
from urllib import urlencode
from HTMLParser import HTMLParser
import re
import googlemaps
start = "7C Smith Street, Boston"
finish = "902 Huntington Ave, Boston"

url = 'http://maps.googleapis.com/maps/api/directions/json?%s' % urlencode((
            ('origin', start),
            ('destination', finish)
 ))
ur = urllib.urlopen(url)
result = json.load(ur)

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
    j = result['routes'][0]['legs'][0]['steps'][i]['html_instructions'] 
    #print j
    k = remove_html_tags(j)
    print k
