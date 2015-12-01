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

TIME_HOUR_OFFSET = -6
CITY_NAME = "chicago"

NUM_HOURS_IN_DAY = 24
NUM_DAYS_IN_WEEK = 7

my_time = time.gmtime(time.time())
my_date = date.fromtimestamp(time.time())

print my_time
print my_date.weekday()

posts = map(int, open("./raw_data/post_times_" + CITY_NAME + ".txt").read().splitlines())
post_freqs = [[0 for col in range(NUM_HOURS_IN_DAY)] for row in range(NUM_DAYS_IN_WEEK)]

for post_unix_time in posts:
    post_time = time.gmtime(post_unix_time + TIME_HOUR_OFFSET*60*60)
    post_date = date.fromtimestamp(post_unix_time + TIME_HOUR_OFFSET*60*60)
    print post_time
    print post_date
    if 23 <= post_time.tm_mday <= 29:
        post_freqs[post_date.weekday()][post_time.tm_hour] += 1
    else:
        print "Date out of range"
    print ""

post_freq_file = open("./freq_data/post_freq_" + CITY_NAME + ".txt", "w")

np.savetxt(fname=post_freq_file, X=post_freqs, fmt='%d', delimiter=' ')