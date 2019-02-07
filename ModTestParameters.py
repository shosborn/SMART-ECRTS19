import SMART
import numpy as np
from random import *

OBLIVIOUS=SMART.Partition.OBLIVIOUS
AWARE_START_PHYS=SMART.Partition.AWARE_START_PHYS
AWARE_START_THREAD=SMART.Partition.AWARE_START_THREAD
AWARE_START_OBLIV=SMART.Partition.AWARE_START_OBLIV
OPTIMAL=SMART.Partition.OPTIMAL
NUM_METHODS=5

#(setUtil, utilMin, utilMax, periodMin, periodMax, rMin, rMax, fMin, fMax, epsilon)

def runParamTest(useOpt, m, binSize, max, beginUtil, utilMin, utilMax, periodMin, periodMax, rMin, rMax, fMin, fMax, epsilon):
    #m=2

    #max=100
    #binSize=.05
    numBins=int(np.ceil(2*m/binSize))
    theBins=[]
    for i in range(0, numBins):
        theBins.append([0]*11)
    #myResults=TaskSetResults(myTaskSet.totalUtil)

    parameterResults=[]


    #for count in range(1, max+1):
    while theBins[0][0]<max:
        #myTaskSet = SMART.TaskSet(.5*m, 0, .3, 10, 100, .7, 1, .7, 1, .1)
        myTaskSet=SMART.TaskSet(beginUtil, utilMin, utilMax, periodMin, periodMax, rMin, rMax, fMin, fMax, epsilon)
        while True:
            #partition and test task set
            while myTaskSet.totalUtil<m:
                myTaskSet.addTask()
            myBin=int(np.floor((myTaskSet.totalUtil-m)/binSize))
            theBins[myBin][0]=theBins[myBin][0]+1
            success=False
            #systemResults=[None] * 11
            #parameterResults.append(systemResults)
            #systemResults[0]=myTaskSet.totalUtil
            for method in range(OBLIVIOUS, OPTIMAL+useOpt):
                myTaskSet.partitionTasks(method)
                theseResults=myTaskSet.partitionList[method].testUmaFunk(m)
                theBins[myBin][method]=theBins[myBin][method]+theseResults[SMART.UMA_RESULT]
                theBins[myBin][method+NUM_METHODS] = theBins[myBin][method+NUM_METHODS] + theseResults[SMART.FUNK_RESULT]
                #systemResults[method]=theseResults[SMART.UMA_RESULT]
                #systemResults[method+NUM_METHODS]=theseResults[SMART.FUNK_RESULT]
                #if theseResults[SMART.UMA_RESULT] or theseResults[SMART.FUNK_RESULT]:
                if theseResults[SMART.UMA_RESULT] + theseResults[SMART.FUNK_RESULT]>0:
                    success=True
            if success:
                myTaskSet.addTask()
            else:
                break
        # no true results --> add tasks to create dummy systems until reached max level of interest
        totalUtil=myTaskSet.totalUtil
        '''
        while totalUtil<1*m:
            systemResults = [None] * 11
            parameterResults.append(systemResults)
            totalUtil=totalUtil+random() * (myTaskSet.utilMax - myTaskSet.utilMin) + myTaskSet.utilMin
            systemResults[0]=totalUtil
            for i in range (1, 11):
                systemResults[i]=False
        '''
        while totalUtil<2*m:
            totalUtil=totalUtil+random() * (myTaskSet.utilMax - myTaskSet.utilMin) + myTaskSet.utilMin
            myBin = int(np.floor((totalUtil - m) / binSize))
            theBins[myBin][0]=theBins[myBin][0]+1
    #for sysResult in parameterResults:
     #    print(sysResult)

    #for i in range (0, len(theBins)):
    #    print (m+i*binSize, theBins[i])

    return theBins
