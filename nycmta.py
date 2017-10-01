from google.transit import gtfs_realtime_pb2
import urllib
from pprint import pprint
from protobuf_to_dict import protobuf_to_dict

#this of stations:
#http://mtaapi.herokuapp.com/stations
#york is F18S and F18N
#high is A40S and A40N

#creates the feed

#URL has API key so keep it in a different file
feed_url = open('url.txt')

feed = gtfs_realtime_pb2.FeedMessage()
response = urllib.urlopen(feed_url.read())
feed.ParseFromString(response.read())

#turns the feed into a dictionary
useful_dict = protobuf_to_dict(feed)

#prints the dicionary just to see what it says
#probably ok to cut this once you figure all of this stuff out
with open('output7.txt', 'wt') as out:
    pprint(useful_dict, stream=out)

#just prints it to the terminal to make it easy to quickly see
#that this worked
pprint(useful_dict)
