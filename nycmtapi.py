#sudo apt-get install python-pip
#sudo -H pip install gtfs-realtime-bindings
from google.transit import gtfs_realtime_pb2
import urllib
from pprint import pprint
#sudo -H pip install protobuf_to_dict
from protobuf_to_dict import protobuf_to_dict
from itertools import chain

#for deciding if the arduino should light up
import datetime
#for comparing the arrival times
import time

#imports the url variables from config.py in the same folder
from config import *

#for talking to arduino
#******this is actually the pyserial library
import serial

from neopixel import *

#variables to hold the lists
arrival_times_york_south = []
arrival_times_york_north = []
arrival_times_high_south = []
arrival_times_high_north = []

#variable to hold the string to send to arduino
light_list = []

# LED strip configuration:
LED_COUNT      = 8      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()





#function to scrape the MTA site and add the arrival times to arrival_times lists
def grabber(station_ID, station_URL):

    try:
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

    #if there is an error getting an MTA feed it still returns something
    #instead of borking the entire process
    except:
        print "Some sort of error getting the %s data" % station_ID
        arrival_times_station = []
        return arrival_times_station

#functionto convert arrival_times lists to lit LEDs
def lighter(arrival_list, light_one, light_two, light_three, light_four, line_R, line_G, line_B):
    #walk through the numbers in the list
    for item in arrival_list:
        #convert the number to a number and see if it is in this
        if 1 <= int(item) <= 8:
            #if it is, turn on the corresponding LED in the correct color
            strip.setPixelColorRGB(light_one, line_R, line_G, line_B)
        elif 8 < int(item) <= 12:
            strip.setPixelColorRGB(light_two, line_R, line_G, line_B)
        elif 12 < int(item) <=17:
            strip.setPixelColorRGB(light_three, line_R, line_G, line_B)
        elif 17 < int(item) <=25:
            strip.setPixelColorRGB(light_four, line_R, line_G, line_B)
        else:
            pass

    #clearn out arrival_times list for the next time around
    #only relevant when this becomes a loop
    arrival_list = []

#to turn off the lights when it is off time
def blackout():
    #figure out the current date and time
    d = datetime.datetime.now()
    #during the week
    if d.weekday() in range(0, 6):
        #is it between 7am and 9pm
        #DONT USE () FOR HOURS
        if d.hour in range(8, 22):
            print "lights would be on weekday"
        #turn off all of the lights
        else:
            for i in range(LED_COUNT):
                strip.setPixelColorRGB(i, 0, 0, 0)
            print "lights would be off"

    #on the weekend
    elif d.weekday() in range(5, 7):
        #between 8am and 10pm
        if d.hour in range (9, 22):
            print "lights would be on weekend"

        else:
            for i in range(LED_COUNT):
                strip.setPixelColorRGB(i, 0, 0, 0)
            print "lights would be off weekend"
    else:
        print "date error"




while True:

    arrival_times_york_south = grabber('F18S', URL_F)
    arrival_times_york_north = grabber('F18N', URL_F)
    arrival_times_high_south = grabber('A40S', URL_AC)
    arrival_times_high_north = grabber('A40N', URL_AC)

    #debugging
    print arrival_times_york_south
    print arrival_times_york_north
    print arrival_times_high_south
    print arrival_times_high_north

    lighter(arrival_times_york_south, 0, 1, 2, 3, 140, 255, 0)
    lighter(arrival_times_york_north, 4, 5, 6, 7, 140, 255,0)
    lighter(arrival_times_high_south, 8, 9, 10, 11, 0, 0, 255)
    lighter(arrival_times_high_north, 12, 13, 14, 15, 0, 0, 255)

    blackout()

    strip.show()

    print "sleeping for 20 seconds"
    time.sleep(20)
