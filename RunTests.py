#!/usr/bin/python3

import ModTestParameters
import SMART
import sys
import csv

M = int(sys.argv[1])
TASK_TARGET = int(sys.argv[2])

ENABLE_OPTIMAL = bool(int(sys.argv[4]))
FILE_OUT = sys.argv[5]

#(setUtil, utilMin, utilMax, periodMin, periodMax, rMin, rMax, fMin, fMax, epsilon)


STEP = .05
#max=1000

#coreCounts=[4, 8, 16, 32]

#resilRanges=[(.65, 1),(.7, 1), (.75, 1), (.8, 1)]

#friendlyRanges=[(.65, 1),(.7, 1), (.75, 1), (.8, 1)]

utilRanges=[(0, .4), (.3, .7), (.6, 1), (0, 1)] # Low, mid, high, and wide. TODO: Bimodel

#epsilon=[0.01, 0.055, 0.1]

#utilHigh=1
#u=[]
#u.append(utilLow)
#u.append(utilHigh)

#test values

setsCompleted=1

# TEMP
e = 0
r = fr = [0,0]

for u in utilRanges:
      paramResults = ModTestParameters.runParamTest(ENABLE_OPTIMAL, M, STEP, TASK_TARGET, .5 * M, u[0], u[1], 10, 100, r[0], r[1], fr[0], fr[1], e)
      with open(FILE_OUT, "a") as f:
          print("*****", file=f) # Sample delimiter
          print(M, ",", STEP, ",", TASK_TARGET, ",", u[0], ",", u[1], ",", 10, ",", 100, ",", r[0], ",", r[1], ",", fr[0], ",", fr[1], ",", e, file=f)
          csvWriter = csv.writer(f)
          binSize = M
          for row in paramResults:
              csvWriter.writerow([binSize] + row)
              binSize += STEP
      # User-visible status
      print(FILE_OUT, setsCompleted, u[0], u[1])
      setsCompleted += 1

print(FILE_OUT, "complete!")
