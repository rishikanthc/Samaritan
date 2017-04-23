import json, urllib
from urllib import urlencode
from HTMLParser import HTMLParser
import re
import googlemaps
#start = "7C Smith Street, Boston"
#finish = "902 Huntington Ave, Boston"



def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def getDirections(start, finish):
	url = 'http://maps.googleapis.com/maps/api/directions/json?%s' % urlencode((
		('origin', start),
		('destination', finish)
		))
	ur = urllib.urlopen(url)
	result = json.load(ur)
	k = ""
	for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
		j = result['routes'][0]['legs'][0]['steps'][i]['html_instructions'] 
		#print j
		k = k + ', ' + remove_html_tags(j)
		# print k
	if len(k) == 0:
		k = "Sorry, couldn't find the said address"
	return k

if __name__ == "__main__":
	tdir = getDirections("Rutgers", "Edison")
	print tdir
