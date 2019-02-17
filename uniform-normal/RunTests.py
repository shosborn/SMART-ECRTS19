#!/usr/bin/python3

import ModTestParameters
import SMART
import sys
import csv
import os.path

# Required
M = int(sys.argv[1])
TASK_TARGET = int(sys.argv[2])
FILE_OUT = sys.argv[3]

if os.path.isfile(FILE_OUT):
    print("Output file " + FILE_OUT + " already exists. Aborting...")
    exit(1)

# Optional multipliers
ENABLE_OPTIMAL = bool(int(sys.argv[4])) if len(sys.argv) > 5 else False 
EPSILON = float(sys.argv[9]) if len(sys.argv) >= 10 else -1
UNIFORM_NORMAL = bool(int(EPSILON) + 1)
if UNIFORM_NORMAL:
    STRENGTH_DIST_BASE = float(sys.argv[5])
    STRENGTH_DIST_CEIL = float(sys.argv[6])
    FRIEND_DIST_BASE = float(sys.argv[7])
    FRIEND_DIST_CEIL = float(sys.argv[8])
else:
    STRENGTH_STDEV_MULTIPLIER = int(sys.argv[5]) if len(sys.argv) >= 7 else 1
    FRIEND_STDEV_MULTIPLIER = int(sys.argv[6]) if len(sys.argv) >= 7 else 1

# These parameters are derived from a statistical analysis of experimental results
FRIEND_MEAN = STRENGTH_MEAN = 0.715825523745
FRIEND_STDEV = 0.0426836366557
STRENGTH_STDEV = 0.130921998163

# These are fixed parameters chosen subjectively
STEP = .05
utilRanges=[(0, 1), (0, .4), (.3, .7), (.6, 1)] # Wide, low, mid, high. TODO: Bimodel

setsCompleted = 1
for utilBound in utilRanges:
    if UNIFORM_NORMAL:
        paramResults = ModTestParameters.runParamTest(ENABLE_OPTIMAL, M, STEP, TASK_TARGET, .5 * M, utilBound[0], utilBound[1], 10, 100, STRENGTH_DIST_BASE, STRENGTH_DIST_CEIL, FRIEND_DIST_BASE, FRIEND_DIST_CEIL, EPSILON)
    else:
        paramResults = ModTestParameters.runParamTest(ENABLE_OPTIMAL, M, STEP, TASK_TARGET, .5 * M, utilBound[0], utilBound[1], 10, 100, STRENGTH_MEAN, STRENGTH_STDEV * STRENGTH_STDEV_MULTIPLIER, FRIEND_MEAN, FRIEND_STDEV * FRIEND_STDEV_MULTIPLIER, 0)

    with open(FILE_OUT, "a") as f:
        print("*****", file=f) # Sample delimiter
        csvWriter = csv.writer(f)
        if UNIFORM_NORMAL:
            csvWriter.writerow([M, STEP, TASK_TARGET, utilBound[0], utilBound[1], 10, 100, STRENGTH_STDEV * STRENGTH_STDEV_MULTIPLIER, FRIEND_STDEV * FRIEND_STDEV_MULTIPLIER)
        else:
            csvWriter.writerow([M, STEP, TASK_TARGET, utilBound[0], utilBound[1], 10, 100, STRENGTH_DIST_BASE, STRENGTH_DIST_CEIL, FRIEND_DIST_BASE, FRIEND_DIST_CEIL, EPSILON])
        binSize = M
        for row in paramResults:
            csvWriter.writerow([binSize] + row)
            binSize += STEP
    # User-visible status
    if UNIFORM_NORMAL:
        print(FILE_OUT, setsCompleted, utilBound[0], utilBound[1], STRENGTH_DIST_BASE, STRENGTH_DIST_CEIL, FRIEND_DIST_BASE, FRIEND_DIST_CEIL, EPSILON)
    else:
        print(FILE_OUT, setsCompleted, utilBound[0], utilBound[1], STRENGTH_STDEV * STRENGTH_STDEV_MULTIPLIER, FRIEND_STDEV * FRIEND_STDEV_MULTIPLIER)
    setsCompleted += 1

print(FILE_OUT, "Complete!")
