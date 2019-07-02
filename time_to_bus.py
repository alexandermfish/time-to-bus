
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToJson
import datetime
import urllib.request
import json
import time


feed = gtfs_realtime_pb2.FeedMessage()
response = urllib.request.urlopen('https://gtfsrt.api.translink.com.au/Feed/SEQ')
feed.ParseFromString(response.read())
counter =0
json_obj_string = MessageToJson(feed)
for entity in feed.entity:
  if entity.HasField('trip_update'):
      counter+=1

data = json.loads(json_obj_string)

#print (json_obj_string)
#print (data['entity']['tripUpdate'])
#print(data['entity'][0]['tripUpdate']['stopTimeUpdate'][0])
def next_busses_at_stop(stop_code_string):
    time_until = list()
    for trips in data['entity']:
        if 'tripUpdate' in trips: #checks to make sure the dict has the key tripUpdate, as not all entrys in data.entity are trips
            if 'stopTimeUpdate' in trips['tripUpdate']:
                for stops in trips['tripUpdate']['stopTimeUpdate']:
                    #print(str(stops['stopId']))
                    
                    if stops['stopId'] == stop_code_string.lstrip('0'):
                        #print(stops)
                        arrival_time_posix = int(stops['arrival']['time'])
                        arrival_time_posix_GMT = arrival_time_posix# + 36000 Unnecessary, translink provides epoch time using our timezone (GMT+10)
                        seconds_until =  arrival_time_posix_GMT-int(time.time())
                        minutes_until = int(seconds_until/60)
                        time_until.append(minutes_until)
                        print("Time until: ~" +str( minutes_until)+ " minutes")
                        #convert to readable
                        print(
                            "Exact Datetime of arrival: "+datetime.datetime.fromtimestamp(arrival_time_posix_GMT).strftime('%Y-%m-%d %H:%M:%S')
                        )
    return time_until

            #print(trips['tripUpdate']['stopTimeUpdate']) #prints the 0th index of entity.trips.tripupdate.stoptimeupdate for each entry of trips

time_until = next_busses_at_stop('10702')
time_until.sort
print(time_until)

