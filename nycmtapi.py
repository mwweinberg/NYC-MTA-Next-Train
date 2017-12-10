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

#for grabber
import math
import os
import traceback

#imports the url variables from config.py in the same folder
from config import *

from neopixel import *

#for the pause button
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#variables to hold the lists
arrival_times_york_south = []
arrival_times_york_north = []
arrival_times_high_south_a = []
arrival_times_high_north_a = []
arrival_times_high_south_c = []
arrival_times_high_north_c = []

#variable to hold the string to send to arduino
light_list = []

# LED strip configuration:
LED_COUNT      = 9      # Number of LED pixels.
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

#GPIO set up at pin 23
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#variables to hold the station IDs
HighS = ['A40S']
HighN = ['A40N']
YorkS = ['F18S']
YorkN = ['F18N']


#function to scrape the MTA site and add the arrival times to arrival_times lists

def grabber(station_ID, station_URL, station_line):

	times = []
	out = ''

	try:
		mtafeed = gtfs_realtime_pb2.FeedMessage()
		#response = urllib.urlopen('http://datamine.mta.info/mta_esi.php?key=' + MTA_KEY + '&feed_id=26')
		response = urllib.urlopen(station_URL)
		mtafeed.ParseFromString(response.read())
		current_time = datetime.datetime.now()
		for stop in station_ID:
			for entity in mtafeed.entity:
				if entity.trip_update.trip.route_id == station_line:
					if entity.trip_update:
						for update in entity.trip_update.stop_time_update:
							if update.stop_id == stop:
								time = update.arrival.time
								if time <= 0:
									time = update.departure.time

								time = datetime.datetime.fromtimestamp(time)
								time = math.trunc(((time - current_time).total_seconds()) / 60)
								times.append(time)
			times.sort()
			for time in times:
				if time < 0:
					times.remove(time)
			for time in times[:NUM_TRAINS]:
				out+=str(time)
				out+=str(',')
			out = out[:-1]
			print times

			return times

			times = []


	except Exception:
		print traceback.format_exc()
		print "Some sort of error getting the %s data" % station_ID
		times = []
		return times


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

#for the pause button
def pause_button(channel):
    print "pausing"
    for i in range(LED_COUNT):
        strip.setPixelColorRGB(i, 0, 0, 0)
    strip.show()
    #time is in seconds
    time.sleep(30)


#checking for the pause button
GPIO.add_event_detect(23, GPIO.FALLING, callback=pause_button, bouncetime=300)

while True:

    arrival_times_york_south = grabber(YorkS, URL_F,'F')
    arrival_times_york_north = grabber(YorkN, URL_F,'F')
    arrival_times_high_south_a = grabber(HighS, URL_AC, 'A')
    arrival_times_high_north_a = grabber(HighN, URL_AC, 'A')
    arrival_times_high_south_c = grabber(HighS, URL_AC, 'C')
    arrival_times_high_north_c = grabber(HighN, URL_AC, 'C')

    lighter(arrival_times_york_south, 0, 1, 2, 3, 140, 255, 0)
    lighter(arrival_times_york_north, 4, 5, 6, 7, 140, 255,0)
    lighter(arrival_times_high_south_a, 8, 9, 10, 11, 0, 0, 255)
    lighter(arrival_times_high_north_a, 12, 13, 14, 15, 0, 0, 255)
    lighter(arrival_times_high_south_c, 16, 17, 18, 19, 0, 0, 255)
    lighter(arrival_times_high_north_c, 20, 21, 22, 23, 0, 0, 255)



    blackout()

    strip.show()

    print "sleeping for 20 seconds"
    time.sleep(20)
