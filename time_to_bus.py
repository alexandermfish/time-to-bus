
from google.transit import gtfs_realtime_pb2
import datetime
import urllib.request
import time


feed = gtfs_realtime_pb2.FeedMessage()
response = urllib.request.urlopen('https://gtfsrt.api.translink.com.au/Feed/SEQ')
feed.ParseFromString(response.read())

#accepts a stop code, returns a list of bus times in posix epoch format
def next_busses_at_stop_posix_time(stop_code_string):
    time_posix_list = list()
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trips = entity.trip_update
            for live_bus in trips.stop_time_update:
                if live_bus.stop_id == stop_code_string.lstrip('0'):
                    arrival_time_posix = int(live_bus.arrival.time)
                    time_posix_list.append(arrival_time_posix)
    time_posix_list.sort()
    return time_posix_list

#accepts a list of posix epoch times, returns a list of minutes until each corresponding posix epoch time
def minutes_until_from_posix(time_posix_list):
    time_until =[]
    for time_posix in time_posix_list:
        seconds_until =  time_posix-int(time.time())
        minutes_until = int(seconds_until/60)
        time_until.append(minutes_until)
    return time_until

#accepts a list of epoch times and prints out the exact datetime in human readable format
def print_exact_datetime(time_posix_list):
    for time_posix in time_posix_list:
        print("Exact Datetime of arrival: "+datetime.datetime.fromtimestamp(time_posix).strftime('%Y-%m-%d %H:%M:%S'))

#accepts a stop code, returns a list of minutes until the next busses at that stop
def time_to_bus(stop_code_string):
    timesuntilposix=next_busses_at_stop_posix_time(stop_code_string)
    timesuntil=minutes_until_from_posix(timesuntilposix)
    return timesuntil

#accepts a list of times in minutes until format, returns a string in human readable format of those times
def times_readable(time_until_list):
    times =[]
    times.append ("The next busses are ")
    for time in time_until_list:
        times.append(str(time))
        times.append(" minutes, ")
    grammar_position = len(times) -2
    times.insert(grammar_position, "and ")
    times[len(times)-1] = " minutes "
    times.append("away")
    
    times_string = "".join(times)

    return times_string
        




print_exact_datetime(next_busses_at_stop_posix_time('010702'))

times_until_list = time_to_bus('010702')
print(times_readable(times_until_list))


