#from PIL import Image, ImageFont, ImageDraw
from google.transit import gtfs_realtime_pb2
#import nyct_subway_pb2
import urllib
import datetime
from time import sleep
import math
import os
from config import *
import traceback


HighN = ['A40S']


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

while True:
	grabber(HighN, URL_AC, 'C')
