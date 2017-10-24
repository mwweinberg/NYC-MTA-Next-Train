#sudo -H pip2 install gtfs-realtime-bindings
from google.transit import gtfs_realtime_pb2
import urllib
from pprint import pprint
#sudo -H pip2 install protobuf_to_dict
from protobuf_to_dict import protobuf_to_dict
from itertools import chain

#for comparing the arrival times
#import datetime
import time
#import dateutil.relativedelta

#current works with python 2

#this of stations:
#http://mtaapi.herokuapp.com/stations
#york is F18S and F18N
#high is A40S and A40N

#used D03N to test in the past
station_one = 'D03N'

#creates the feed

#URL has API key so keep it in a different file
feed_url = open('url.txt')

feed = gtfs_realtime_pb2.FeedMessage()
response = urllib.urlopen(feed_url.read())
feed.ParseFromString(response.read())

#turns the feed into a dictionary
useful_dict = protobuf_to_dict(feed)
#just for troubleshooting
#print useful_dict

#this will print out everything that comes through the feed for troubleshooting/planning purposes into a file
#with open('useful_dict.txt', 'wt') as out:
 #    pprint(useful_dict, stream=out)

#this is the list of sub elements in useful_dict. basically it makes useful_dict slightly more manageable
useful_list = []

#list of arrival times to be filled by extracting info from small_list
arrival_times = []

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

#extracts the times from the small_list and adds to arrival_times list
for i in small_list:
    #this is the arrival time of each train
    the_time = i['arrival']['time']
    #the_time - time.time gives you the seconds between arrival time and current time
    arrival_time_in_minutes = (int(the_time) - int(time.time()))/60
    #add arrival time to arrival_times list
    arrival_times.append(arrival_time_in_minutes)
    #just for troubleshooting
    print arrival_time_in_minutes
    

#just for debugging
print arrival_times
