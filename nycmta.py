from google.transit import gtfs_realtime_pb2
import urllib
from pprint import pprint
from protobuf_to_dict import protobuf_to_dict
from itertools import chain

#this of stations:
#http://mtaapi.herokuapp.com/stations
#york is F18S and F18N
#high is A40S and A40N

station_one = 'D03N'

#creates the feed

#URL has API key so keep it in a different file
feed_url = open('url.txt')

feed = gtfs_realtime_pb2.FeedMessage()
response = urllib.urlopen(feed_url.read())
feed.ParseFromString(response.read())

#turns the feed into a dictionary
useful_dict = protobuf_to_dict(feed)



useful_list = []

#walks through each train entry to see if it is an active train

for i in range (len(useful_dict['entity'])):
    #this seems to be necessary, I'm not sure why
    if useful_dict['entity'][i]['id']:
        #adds the arrival information to useful_list
        try:
            useful_list.append(useful_dict['entity'][i]['trip_update']['stop_time_update'])
        #if it is an entry that it not an active train, ignores
        except KeyError:
            pass

#pulls the entries tied to specific stops
small_list = [ i for i in chain.from_iterable(useful_list) if i['stop_id'] == station_one ]

pprint(small_list)
