"""
File: curve_fit_data.py (Project - InstaFreq)
Authors:    Brandon Walsh   brando12@umbc.edu
            Neil Joshi      njoshi2@umbc.edu
            Duke Nguyen     du2@umbc.edu
Date: 12/1/15
Class: CMSC 455, Fall 2015
Instructor: Tyler Simon
Section: 02

    This script uses numpy to easily generate a polynomial curve
    that fits the post frequency data for every day of the week

"""

import numpy as np
import matplotlib.pyplot as plt

CITY_NAME = "Chicago"
POLY_DEGREE_PER_DAY = 10
POLY_DEGREE_WHOLE_WEEK = 50

SAVE_PLOTS = True

DAYS_OF_THE_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

curve_coef_per_day = []

post_freq_file = open("./freq_data/post_freq_" + CITY_NAME + ".txt")

week_freq = np.loadtxt(fname=post_freq_file, dtype=int, delimiter=' ')

# print week_freq

hours_in_day_x = [i for i in range(24)]

week_freq_concat = []
print type(week_freq[0])

for day in range(len(week_freq)):
    curve_coef_per_day.append(np.polyfit(hours_in_day_x, week_freq[day], POLY_DEGREE_PER_DAY))
    week_freq_concat += week_freq[day].tolist()

curve_data_per_day_file = open("./curve_data/curve_data_per_day_" + CITY_NAME + ".txt", "w")

np.savetxt(fname=curve_data_per_day_file, X=curve_coef_per_day, fmt='%f', delimiter=' ')


hours_in_week_x = [i for i in range(24*7)]

curve_data_whole_week_file = open("./curve_data/curve_data_whole_week_" + CITY_NAME + ".txt", "w")

curve_coef_whole_week = np.polyfit(hours_in_week_x, week_freq_concat, POLY_DEGREE_WHOLE_WEEK)

print np.poly1d(curve_coef_whole_week)

np.savetxt(fname=curve_data_whole_week_file, X=curve_coef_whole_week, fmt='%f', delimiter=' ', newline=' ')

for day in range(len(DAYS_OF_THE_WEEK)):
    fig = plt.figure()
    fig.suptitle(CITY_NAME, fontsize=16, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel("Hour")
    ax.set_ylabel("# Posts")
    ax.set_title(DAYS_OF_THE_WEEK[day])

    xp = np.linspace(0, 24-1, 100)
    p = np.poly1d(curve_coef_per_day[day])
    plt.scatter(hours_in_day_x, week_freq[day])
    plt.plot(hours_in_day_x, week_freq[day], '.', xp, p(xp), '-')

    plt.ylim([0, plt.axes().get_ylim()[1]])
    plt.xlim([0, plt.axes().get_xlim()[1]])

    plt.savefig("./graphs/" + CITY_NAME + "/" + CITY_NAME + "_" + DAYS_OF_THE_WEEK[day] + ".png")
    # plt.show()
    fig.clear()

fig = plt.figure()
fig.suptitle(CITY_NAME, fontsize=16, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel("Hour")
ax.set_ylabel("# Posts")
ax.set_title("Full Week (11/23/15 - 11/29/15)")

xp = np.linspace(0, 24*7-1, 100)
p = np.poly1d(curve_coef_whole_week)
plt.scatter(hours_in_week_x, week_freq_concat)
plt.plot(hours_in_week_x, week_freq_concat, '.', xp, p(xp), '-')

plt.ylim([0, plt.axes().get_ylim()[1]])
plt.xlim([0, plt.axes().get_xlim()[1]])

plt.savefig("./graphs/" + CITY_NAME + "/" + CITY_NAME + "_FullWeek.png")