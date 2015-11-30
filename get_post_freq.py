import time
import numpy as np
from datetime import date

TIME_HOUR_OFFSET = -5

NUM_HOURS_IN_DAY = 24
NUM_DAYS_IN_WEEK = 7

my_time = time.gmtime(time.time())
my_date = date.fromtimestamp(time.time())

print my_time
print my_date.weekday()

posts = []
post_freqs = [[0 for col in range(NUM_HOURS_IN_DAY)] for row in range(NUM_DAYS_IN_WEEK)]

for post in posts:
    post_time = time.gmtime(post.time + TIME_HOUR_OFFSET*60*60)
    post_date = date.fromtimestamp(post.time + TIME_HOUR_OFFSET*60*60)
    print post_time
    print post_date
    if 23 <= post_time.tm_mday <= 29:
        post_freqs[post_date.weekday()][post_time.tm_hour] += 1
    else:
        print "Date out of range"
    print ""

post_freq_file = open("post_freq.txt")

# np.savetxt(fname=post_freq_file, X=post_freqs, fmt='%d', delimiter=' ')
