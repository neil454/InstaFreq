"""
File: get_post_freq.py (Project - InstaFreq)
Authors:    Brandon Walsh   brando12@umbc.edu
            Neil Joshi      njoshi2@umbc.edu
            Duke Nguyen     du2@umbc.edu
Date: 12/1/15
Class: CMSC 455, Fall 2015
Instructor: Tyler Simon
Section: 02

    This script processes the raw Instagram data and generates a
    2D array with post frequency where rows=DAY_OF_WEEK, col=HOUR

"""

import time
from datetime import date
import numpy as np

NUM_HOURS_IN_DAY = 24
NUM_DAYS_IN_WEEK = 7

# Script Parameters (make sure to change both at same time, as they are related!)
TIME_HOUR_OFFSET = -5
CITY_NAME = "DC"

# Get raw post data, read each separate line into an array
raw_post_times = map(int, open("./raw_data/post_times_" + CITY_NAME + ".txt").read().splitlines())

# Initialize the 2D array for the post frequencies
post_freqs = [[0 for col in range(NUM_HOURS_IN_DAY)] for row in range(NUM_DAYS_IN_WEEK)]

# Go through all the raw post times
for raw_post_time in raw_post_times:
    # Convert into UTC time and python date object, offsetting for timezone along the way
    post_time = time.gmtime(raw_post_time + TIME_HOUR_OFFSET*60*60)
    post_date = date.fromtimestamp(raw_post_time + TIME_HOUR_OFFSET*60*60)
    print post_time
    print post_date

    # Check if post is between Nov. 23 and Nov. 29 (for the purposes of this project only)
    if 23 <= post_time.tm_mday <= 29:
        # If it is, iterate the appropriate frequency element in the frequency array
        post_freqs[post_date.weekday()][post_time.tm_hour] += 1
    else:
        # Otherwise, take note of it (lots of these show that the scrape as many unused data)
        print "Date out of range"
    print ""

# Save post frequencies
post_freq_file = open("./freq_data/post_freq_" + CITY_NAME + ".txt", "w")
np.savetxt(fname=post_freq_file, X=post_freqs, fmt='%d', delimiter=' ')