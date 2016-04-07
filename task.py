import requests, urllib2, json
from math import radians, cos, sin, asin, sqrt

places=[]	#Will be the list of all the destinations read from input.txt
distance_dict={};	#Will map the locations to their road distance from origin(IITB)
invalid_list=[]		#will store the places whose road distance from origin(IITB) was not found
straight_distance_dict={};	#Will map the locations to their bird's line distance from origin(IITB)
distancematrix_url='https://maps.googleapis.com/maps/api/distancematrix/json?'
geocode_url='https://maps.googleapis.com/maps/api/geocode/json?'
origin='IIT Bombay'
API_KEY="AIzaSyBv8_O03gYPjkKUh2XvrpxJM2ttB1qQfSA"


def get_destination():
	"""
	Reads input.txt and forms the destination parameter
	which forms a part of the Google Distance Matrix request
	"""
	global places
	file=open("input.txt","r")
	lines = [line.strip() for line in file if line.strip()]
	places=lines
	lines = [word.replace(' ','+') for word in lines]
	file.close()
	return '|'.join(lines)

def get_coordinates(place):
	"""
	Get the latitude and longitude of all the locations
	"""
	payload2={'address':place, 'key':API_KEY}
	response = requests.get(geocode_url,params=payload2)

	resp_json_payload = response.json()
	latitude=resp_json_payload['results'][0]['geometry']['location']['lat']
	longitude=resp_json_payload['results'][0]['geometry']['location']['lng']
	return latitude,longitude

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def print_dict(dictionary):
	for key, value in sorted(dictionary.iteritems(), key=lambda (k,v): (v,k)):
		print key

#PRIMARY TASK

payload1 = {'origins': 'IIT Bombay', 'destinations': get_destination(), 'key':API_KEY}
req = requests.get(distancematrix_url,params=payload1)
info=req.json()

for i in range(0,len(info['rows'][0]['elements'])):
	if info['rows'][0]['elements'][i]['status']=='OK':
		distance_dict[places[i]]=info['rows'][0]['elements'][i]['distance']['value']

	else:
		invalid_list.append(places[i])

print "The places in increasing order of road distance from IIT Bombay are:"
print_dict(distance_dict)

for place in invalid_list:
	print place

#BONUS TASK
origin_lat,origin_lng=get_coordinates(origin)
for place in places:
	lat,lng=get_coordinates(place)
	distance=haversine(origin_lng,origin_lat,lng,lat)
	straight_distance_dict[place]=distance

print "The places in increasing order of bird-line distance from IIT Bombay are:"
print_dict(straight_distance_dict)