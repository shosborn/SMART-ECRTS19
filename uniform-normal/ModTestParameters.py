import SMART
import numpy as np
from random import *

OBLIVIOUS=SMART.Partition.OBLIVIOUS
AWARE_START_PHYS=SMART.Partition.AWARE_START_PHYS
AWARE_START_THREAD=SMART.Partition.AWARE_START_THREAD
AWARE_START_OBLIV=SMART.Partition.AWARE_START_OBLIV
OPTIMAL=SMART.Partition.OPTIMAL
NUM_METHODS=5

def runParamTest(useOpt, m, binSize, max, beginUtil, utilMin, utilMax, periodMin, periodMax, strength_p1, strength_p2, friend_p1, friend_p2, epsilon):

    numBins = int(np.ceil(m/binSize))
    # "theBins": index 0 is number of task sets in bin, following indicies are how many of those are schedulable for various algorithms
    theBins = []
    for i in range(0, numBins):
        theBins.append([0] * 11)

    parameterResults = []

    # Iterate until we've tried at least 'max' task sets at our base utilization
    # Each iteration of this tests at least one task set per bin
    while theBins[0][0] < max:
        myTaskSet = SMART.TaskSet(beginUtil, utilMin, utilMax, periodMin, periodMax, strength_p1, strength_p2, friend_p1, friend_p2, epsilon)
        # Loop until we reach a task set that nothing can schedule
        while True:
            # Make sure we have at least enough utilization to reach the first bin (at m)
            while myTaskSet.totalUtil < m:
                myTaskSet.addTask()
            # Depending on where our utilization fell as we added tasks, we choose a bin
            myBin = int(np.floor((myTaskSet.totalUtil - m) / binSize))
            theBins[myBin][0] += 1 # One more sample for this bin
            # Test if each algorthm can schedule this set
            for method in range(OBLIVIOUS, OPTIMAL+useOpt):
                myTaskSet.partitionTasks(method)
                theseResults = myTaskSet.partitionList[method].testUmaFunk(m)
                # We use two schedulability tests. Make sure to store the results for both.
                theBins[myBin][method] += theseResults[SMART.UMA_RESULT]
                theBins[myBin][method+NUM_METHODS] += theseResults[SMART.FUNK_RESULT]
            # If any algorithm had any successes, keep adding work (and potentially fall into higher bins) until that's not true
            if sum(theBins[myBin][OBLIVIOUS:]):
                myTaskSet.addTask()
            else:
                break
        # If we reach a task set that's unschedulable, assume it's unschedulable for higher utilizations.
        # This step records that assumption for bins after the one that everyone failed on
        # (We could just simulate all the higher-utilization bins, but that's slow.)
        totalUtil = myTaskSet.totalUtil
        while totalUtil < m:
            totalUtil += random() * (myTaskSet.utilMax - myTaskSet.utilMin) + myTaskSet.utilMin
            myBin = int(np.floor((totalUtil - m) / binSize))
            theBins[myBin][0] += 1
    return theBins
