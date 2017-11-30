import gpxpy
import gpxpy.gpx
import gpxpy.geo
import os
import time
import datetime

gpx_file = open(os.path.expanduser('~/Downloads/') + "Morning_Ride.gpx", 'r')
gpx = gpxpy.parse(gpx_file)

def iter_previous_current(points):
    previous = None
    for current in points:
        if previous is not None:
            yield previous, current
        previous = current


for track in gpx.tracks:
    for segment in track.segments:
        print("Total points: {}".format(len(segment.points)))
        for startpoint, endpoint in iter_previous_current(segment.points):
            startepochtime = time.mktime(time.strptime(str(startpoint.time),"%Y-%m-%d %H:%M:%S"))
            endepochtime = time.mktime(time.strptime(str(endpoint.time),"%Y-%m-%d %H:%M:%S"))
## Point at (49.855611,2.396663, 2017-11-26 07:50:36)
            distance = gpxpy.geo.haversine_distance(startpoint.latitude, startpoint.longitude,endpoint.latitude, endpoint.longitude)
            speed = 3.6*(distance/(endepochtime-startepochtime))
            print('point @ time={}s, distance={}m, speed={}Km/h'.format(int(endepochtime-startepochtime), distance, int(speed)))
