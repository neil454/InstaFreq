# -*- coding: utf-8 -*-
from instagram.client import InstagramAPI
from collections import Counter
import unicodedata
import calendar
import datetime
import time
import math
from random import randint
import difflib


###########################################################################
###########################################################################
###########################################################################
#Insta Scaper Code
#CMSC455 Project
#Version 1.0
#Description: scrape instagram posts over a time
#             range in a lat/lng designated 5km area.
###########################################################################
###########################################################################
###########################################################################

def main():
    api = InstagramAPI(client_id='1ed75e7649544ac5b1aacd2a1d6db2b1',
                       client_secret='1b78cda37723445b85f5c6da25469611')

    global text_file

    generatePosts(api, 40.730453, -73.994008, 10, 5000)


#==========================================================================#
#generatePosts: scrapes all posts within a specific 1km zone until the     #
#               designated time in the past is reached.                    #
#==========================================================================#
def generatePosts(api, userLat, userLng, days, sizeinM):

    #Initialize timestamp with current time
    timestamp = getCurrentTime();

    #Get the time difference
    goalTime = getTimeDifference(days)

    #Loop until the last post exceeds the goal time
    while (timestamp > goalTime):

        try:

            rawPosts = api.media_search(distance=sizeinM, count=100, lat=userLat, lng=userLng, max_timestamp=timestamp)
        #except InstagramAPIError, I:
            time.sleep(randint(1,3))
            #rawPosts = api.media_search(distance=1000, count=100, lat=userLat, lng=userLng, max_timestamp=timestamp)
        except:
             while True:
                try:
                    rawPosts = api.media_search(distance=sizeinM, count=100, lat=userLat, lng=userLng, max_timestamp=timestamp)
                except:
                    continue
                break

        #parse the posts to a formatted python array
        posts = parsePosts(rawPosts)

        #break if no posts exist
        if (len(posts) == 0 or len(posts) == 1):
            goalTime = timestamp
        else:
            #Get the last timestamp
            timestamp = posts[len(posts)-1]["time"]
            print timestamp

        #append posts to a larger array here


#==========================================================================#
#parsePosts: parses a single request of posts into our custom array and    #
#            performs important parsing/cleaning operations.               #
#==========================================================================#
def parsePosts(rawPosts):

    posts = []

    for media in rawPosts:

        try:

            #intialize the post dictionary
            post = {'time': 1, 'media_url': "", 'location_name': "", 'location': [1,1]}

            #time created
            post["time"] = datetime_to_timestamp(media.created_time)
            with open("output_newyork.txt", "a") as text_file:
                text_file.write("%s\n" % (str(post["time"])))
            #print post["time"]

            #location id of post
            #post["location_name"] = media.location.name
            #print post["location_name"]

            #lat/lng of post
            #post["location"][0] = media.location.point.latitude
            #post["location"][1] = media.location.point.longitude
            #print str(post["location"][0]) + ', ' + str(post["location"][1])

            #Yelp Validation and extra data
            #name = media.location.name
            #lat = media.location.point.latitude
            #lng = media.location.point.longitude

            #media url
            #post["media_url"] = media.link
            #print post["media_url"]

            posts.append(post)

            #print '--------------------------------'
            
        except UnicodeEncodeError, e:
            #print 'POST NOT IN ENGLISH'
            print ''

    return posts


#HELPER FUNCTIONS
#########################################################################################
####################################################
#Parse a string to tags and eliminate common words
####################################################
def textToTags(text):

    import re
    regex = re.compile('[^a-zA-Z ]')
    text = regex.sub('', text)
    text = text.lower()
    from nltk.corpus import stopwords
    s=set(stopwords.words('english'))

    return filter(lambda w: not w in s,text.split())

####################################################
#Finds the most common words in a string
####################################################
def mostCommonWords(text):
    from collections import Counter
    print Counter(text.split()).most_common()


#####################################################
#Convert datetime to time stamp
#####################################################
def datetime_to_timestamp(dt):
    return calendar.timegm(dt.timetuple())

#####################################################
#Get time difference
#####################################################
def getTimeDifference(days):
    currentTime = int(time.time())
    pastTime = daysToSeconds(days)
    goalTime = currentTime - pastTime
    return goalTime

#####################################################
#Get current unix timestamp
#####################################################
def getCurrentTime():
    return calendar.timegm(time.gmtime())


#####################################################
#Convert days to seconds
#####################################################
def daysToSeconds(days):
    return days * 24 * 60 * 60


#####################################################
#Get a new lat
#####################################################
def shiftLat(lat, offset):

     #Earth’s radius, sphere
     R=6378137

     #Coordinate offsets in radians
     dLat = float(offset)/R

     #OffsetPosition, decimal degrees
     latNew = lat - dLat * 180/math.pi

     return latNew

#####################################################
#Get a new lng
#####################################################
def shiftLng(lat, lng, offset):

     #Earth’s radius, sphere
     R=6378137

     #Coordinate offsets in radians
     dLng = float(offset)/(R*math.cos(math.pi*lat/180))

     #OffsetPosition, decimal degrees
     lngNew = lng + dLng * 180/math.pi

     return lngNew


#####################################################
#km to meters
#####################################################
def kmToMeters(km):
    return km*1000

#####################################################
#Compare to strings and return a percentage
#####################################################
def compareStrings(s1,s2):
    return difflib.SequenceMatcher(None,s1,s2).ratio()

main()
