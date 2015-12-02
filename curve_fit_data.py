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
    that fits the post frequency data for every day of the week,
    and for the whole week. It also uses matplotlib to create graphs.

"""

import numpy as np
import matplotlib.pyplot as plt

DAYS_OF_THE_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Script Parameters
CITY_NAME = "Baltimore"
POLY_DEGREE_PER_DAY = 10        # Default=10
POLY_DEGREE_WHOLE_WEEK = 50     # Default=50
SAVE_GRAPH = False

##### ACTUAL PROGRAM STARTS #####

# STEP 1: Set up the X and Y values to be used for Polynomial Curve Fitting
# Open and load frequency data, use as Y values
post_freq_file = open("./freq_data/post_freq_" + CITY_NAME + ".txt")
Ys_week_freq = np.loadtxt(fname=post_freq_file, dtype=int, delimiter=' ')
# This will eventually be daily frequencies concatenated together (1D array)
Y_week_freq_concat = []

# Generate X values, which are just hours from 0-23 (0-168 for whole week)
X_hours_in_day = [i for i in range(24)]
X_hours_in_week = [i for i in range(24*7)]

# STEP 2: Polynomial Curve Fitting
# Iterate through each day and generate a polynomial curve to fit data for each day
curve_coef_per_day = []
for day in range(len(Ys_week_freq)):
    # Numpy's polyfit() func takes X and Y arrays (1D), and the desired polynomial degree
    curve_coef_per_day.append(np.polyfit(X_hours_in_day, Ys_week_freq[day], POLY_DEGREE_PER_DAY))
    # Concatenate this array while we're here...
    Y_week_freq_concat += Ys_week_freq[day].tolist()

# Save daily curve coefficients in curve_data folder
curve_data_per_day_file = open("./curve_data/curve_data_per_day_" + CITY_NAME + ".txt", "w")
np.savetxt(fname=curve_data_per_day_file, X=curve_coef_per_day, fmt='%f', delimiter=' ')

# Generate a polynomial curve (different degree) for the whole week (168 hours)
curve_coef_whole_week = np.polyfit(X_hours_in_week, Y_week_freq_concat, POLY_DEGREE_WHOLE_WEEK)
# print np.poly1d(curve_coef_whole_week)

# Save it as well
curve_data_whole_week_file = open("./curve_data/curve_data_whole_week_" + CITY_NAME + ".txt", "w")
np.savetxt(fname=curve_data_whole_week_file, X=curve_coef_whole_week, fmt='%f', delimiter=' ', newline=' ')

# STEP 3: Generate graphs from polynomials, using matplotlib
# For each day, plot and save the graph of its data points and its polynomial curve drawn on top
for day in range(len(DAYS_OF_THE_WEEK)):
    # Set up matplotlib figure, title, axis, etc.
    fig = plt.figure()
    fig.suptitle(CITY_NAME, fontsize=16, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel("Hour")
    ax.set_ylabel("# Posts")
    ax.set_title(DAYS_OF_THE_WEEK[day])

    # xp = 100 points between 0 and 23, used as X values for drawing curve
    xp = np.linspace(0, 24-1, 100)
    # p = polynomial function in usable format, p(xp) used as Y values for drawing curve
    p = np.poly1d(curve_coef_per_day[day])
    # First, plot a scatter of the frequency data points
    plt.scatter(X_hours_in_day, Ys_week_freq[day])
    # Then, draw the curve on top
    plt.plot(X_hours_in_day, Ys_week_freq[day], '.', xp, p(xp), '-')

    # Limit the axis to positive x and y, as matplotlib tends to grow outside of these automatically
    plt.ylim([0, plt.axes().get_ylim()[1]])
    plt.xlim([0, plt.axes().get_xlim()[1]])

    # Save graph and clear the figure for next day
    if SAVE_GRAPH:
        plt.savefig("./graphs/" + CITY_NAME + "/" + CITY_NAME + "_" + DAYS_OF_THE_WEEK[day] + ".png")
    # plt.show()
    fig.clear()

# Do the same stuff as above, but with the whole week data concatenated
fig = plt.figure()
fig.suptitle(CITY_NAME, fontsize=16, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel("Hour")
ax.set_ylabel("# Posts")
ax.set_title("Full Week (11/23/15 - 11/29/15)")

xp = np.linspace(0, 24*7-1, 100)
p = np.poly1d(curve_coef_whole_week)
plt.scatter(X_hours_in_week, Y_week_freq_concat)
plt.plot(X_hours_in_week, Y_week_freq_concat, '.', xp, p(xp), '-')

plt.ylim([0, plt.axes().get_ylim()[1]])
plt.xlim([0, plt.axes().get_xlim()[1]])

if SAVE_GRAPH:
    plt.savefig("./graphs/" + CITY_NAME + "/" + CITY_NAME + "_FullWeek.png")
