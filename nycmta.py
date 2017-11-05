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

#imports the url variables from config.py in the same folder
from config import *

#variables to hold the lists
arrival_times_york_south = []
arrival_times_york_north = []
arrival_times_high_south = []
arrival_times_high_north = []

#variable to hold the string to send to arduino
light_list = []


#function to scrape the MTA site and add the arrival times to arrival_times lists
def grabber(station_ID, station_URL):

    #grabs the feed
    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.urlopen(station_URL)
    feed.ParseFromString(response.read())

    #turns the feed into a dictionary
    useful_dict = protobuf_to_dict(feed)

    #this is the list of sub elements in useful_dict. basically it makes useful_dict slightly more manageable
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
    small_list_station = [ i for i in chain.from_iterable(useful_list) if i['stop_id'] == station_ID ]

    #list of arrival times to be filled by extracting info from small_list
    arrival_times_station = []
    #extracts the times from the small_list and adds to arrival_times list
    for i in small_list_station:
        #this is the arrival time of each train
        the_time = i['arrival']['time']
        #the_time - time.time gives you the seconds between arrival time and current time
        arrival_time_in_minutes = (int(the_time) - int(time.time()))/60
        #add arrival time to arrival_times list
        arrival_times_station.append(arrival_time_in_minutes)


    return arrival_times_station

#functionto convert arrival_times lists to a string to send to arduino
def lighter(arrival_list, light_one, light_two, light_three, light_four):
    #walk through the numbers in the list
    for item in arrival_list:
        #convert the number to a number and see if it is in this
        if 1 <= int(item) <= 8:
            #if it is, add it to the list to send to the arduino
            light_list.append(light_one)
        elif 8 < int(item) <= 12:
            light_list.append(light_two)
        elif 12 < int(item) <=17:
            light_list.append(light_three)
        elif 17 < int(item) <=25:
            light_list.append(light_four)
        else:
            pass

    #clearn out arrival_times list for the next time around
    #only relevant when this becomes a loop
    arrival_list = []



arrival_times_york_south = grabber('F18S', URL_F)
arrival_times_york_north = grabber('F18N', URL_F)
arrival_times_high_south = grabber('A40S', URL_AC)
arrival_times_high_north = grabber('A40N', URL_AC)

#debugging
print arrival_times_york_south
print arrival_times_york_north
print arrival_times_high_south
print arrival_times_high_north

lighter(arrival_times_york_south, 'a', 'b', 'c', 'd')
lighter(arrival_times_high_north, 'e', 'f', 'g', 'h')
lighter(arrival_times_high_south, 'i', 'j', 'k', 'l')
lighter(arrival_times_high_north, 'm', 'n', 'o', 'p')

#debugging
print light_list
