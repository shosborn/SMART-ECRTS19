from typing import List

import numpy as np
import sys

# constants for columns of file
FIRST_PROG = 0
SECOND_PROG = 1
FIRST_CORE = 2
SECOND_CORE = 3
TOTAL_TRIALS = 4
TIME = 5
RUN_ID = 6
THIS_TRIAL = 7
times = []

print("first", "second", "max", "per99", "per98", "per95", "mean", "Std. Dev")

with open(sys.argv[1]) as f:
    for line in f:
        lineArr = line.split()
        times.append(int(lineArr[TIME]))
        if int(lineArr[THIS_TRIAL]) == (int(lineArr[TOTAL_TRIALS]) - 1):
            # calculate stuff and output list
            mean = np.mean(times)
            max = np.amax(times)
            per99 = np.percentile(times, 99)
            per98 = np.percentile(times, 98)
            per97 = np.percentile(times, 97)
            per95 = np.percentile(times, 95)
            stdDev = np.std(times)
            print(lineArr[FIRST_PROG], lineArr[SECOND_PROG], max, per99, per98, per95, mean, stdDev)
            # reset stuff
            times = []
