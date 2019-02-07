#!/usr/bin/python

import ModTestParameters
import SMART
import sys
m=int(sys.argv[1])
max=int(sys.argv[2])
e=sys.argv[3]
useOpt=int(sys.argv[4])
fileOut=sys.argv[5]+".txt"

#(setUtil, utilMin, utilMax, periodMin, periodMax, rMin, rMax, fMin, fMax, epsilon)


binSize=.05
#max=1000

#coreCounts=[4, 8, 16, 32]

resilRanges=[(.65, 1),(.7, 1), (.75, 1), (.8, 1)]

friendlyRanges=[(.65, 1),(.7, 1), (.75, 1), (.8, 1)]

utilRanges=[(0, .4), (.3, .7), (0, 1)]

#epsilon=[0.01, 0.055, 0.1]

#utilHigh=1
#u=[]
#u.append(utilLow)
#u.append(utilHigh)

#test values
'''
binSize=.05
max=10
coreCounts=(1, 2, 4)
resilRanges=[(.6, .9), (.7, 1)]
friendlyRanges=[(.6, .9), (.7, 1)]
utilRanges=[(0, .4), (.3, .7)]
epsilon=[0, .1]
'''

setsCompleted=1

for x in range (0, 1):
   for r in resilRanges:
        for fr in friendlyRanges:
            for u in utilRanges:
                for z in range(0, 1):
                    paramResults=[]
                    #def runParamTest(m, binSize, max, beginUtil, utilMin, utilMax, periodMin, periodMax, rMin, rMax,
                    #                 fMin, fMax, epsilon):
                    #paramResults=ModTestParameters.runParamTest(m, binSize, max, .5*m, u[0], u[1], 10, 100, r[0], r[1], f[0], f[1], e)
                    paramResults = ModTestParameters.runParamTest(useOpt, m, binSize, max, .5 * m, u[0], u[1], 10, 100, r[0],
                                                                  r[1], fr[0], fr[1], e)
                    #print("Parameter set completed:")
                    print(fileOut, setsCompleted, u[0], u[1], 10, 100, r[0], r[1], fr[0], fr[1], e)
                    setsCompleted=setsCompleted+1
                    with open(fileOut, "a") as f:
                        print("*****", file=f)
                        print(m, ",", binSize, ",", max, ",", u[0], ",", u[1], ",", 10, ",", 100, ",", r[0], ",", r[1], ",", fr[0], ",", fr[1], ",", e, file=f)
                    #f.write(m, binSize, max, u[0], u[1], 10, 100, r[0], r[1], f[0], f[1], e)
                    #f.write("%d, %f, %d, %f, %f, %d, %d, %f, %f, %f, %f, %f \n", m, binSize, max, u[0], u[1], 10, 100, r[0], r[1], f[0], f[1], e)
                        for i in range (0, len(paramResults)):
                            if paramResults[i][0]>0:
                                #print(m+i*binSize, paramResults[i], file=f)
                                print(m+i*binSize, file=f, end="")
                                print(",", file=f, end="")
                                for j in range(0, len(paramResults[i])):
                                    print(paramResults[i][j], file=f, end="")
                                    if j<len(paramResults[i])-1:
                                        print(",", file=f, end="")
                                    else:
                                        print("", file=f)

print(fileOut, "complete!")
