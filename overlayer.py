import sys
import os
import time
import gpxpy
import gpxpy.gpx
import gpxpy.geo
import datetime
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from ffmpy3 import FFmpeg
from collections import OrderedDict



def iter_previous_current(points):
    previous = None
    for current in points:
        if previous is not None:
            yield previous, current
        previous = current

#gpx_file = open(os.path.expanduser('~/Downloads/') + "Morning_Ride.gpx", 'r')
with open(os.path.expanduser(sys.argv[1])) as gpx_file:
    gpx = gpxpy.parse(gpx_file)


    catfile = open('catfile.txt', 'w')

    files = OrderedDict()
    filesbyname = ""
    counter = 1
    for track in gpx.tracks:
        for segment in track.segments:
            print("Total points: {}".format(len(segment.points)))
            for startpoint, endpoint in iter_previous_current(segment.points):
                startepochtime = time.mktime(time.strptime(str(startpoint.time),"%Y-%m-%d %H:%M:%S"))
                endepochtime = time.mktime(time.strptime(str(endpoint.time),"%Y-%m-%d %H:%M:%S"))
    ## Point at (49.855611,2.396663, 2017-11-26 07:50:36)
                distance = gpxpy.geo.haversine_distance(startpoint.latitude, startpoint.longitude,endpoint.latitude, endpoint.longitude)
                speed = 3.6*(distance/(endepochtime-startepochtime))
                print('point {}: time={}s, distance={}m, speed={}Km/h'.format(counter, int(endepochtime-startepochtime), distance, int(speed)))
                #filename = str(counter) + ".jpg"
                with Image(width=200, height=150, background=Color('transparent')) as img:
                    with Drawing() as banner:
                        #banner.fill_color = Color('li')
                        banner.stroke_color = Color('white')
                        banner.font_size = 40
                        banner.text(x=25, y=75, body=str(int(speed)) + "Km/h")
                        banner(img)
                        img.format = 'jpeg'
                        # do stuff here
                        img.save(filename=str(counter) + ".jpg")
                        print("Frame: {}, lenght: {}s".format(counter, (endepochtime-startepochtime)))
                        files.update({str(counter) + ".jpg" : None})
                        catfile.write("file '" + str(counter) + ".mp4'\n")
                        #catfile.write("duration {}\n".format(str(int(endepochtime-startepochtime))))
                        ff=FFmpeg(inputs={str(counter) + ".jpg": "-y -loglevel quiet -loop 1 -r 30"}, outputs={str(counter) + ".mp4":"-c:v libx264 -vf fps=30 -pix_fmt yuv420p -t " + str(int(endepochtime-startepochtime))})
                        print(ff.cmd)
                        ff.run()

                counter +=1
    #print(files)
    catfile.close()

    ffcat = FFmpeg(
        inputs={'catfile.txt': '-y -f concat -safe 0'},
        outputs={'final.mp4':'-c copy'}
    )
    print(ffcat.cmd)
    ffcat.run()
