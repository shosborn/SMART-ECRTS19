from random import *
import numpy as np
import itertools

# def main():
#   TaskSet(8, .7, 1, 10, 100, .7, 1, .7, 1, .1)


FAKE_ZERO = 0.00000000001
UMA_RESULT=0
FUNK_RESULT=1

# These parameters are derived from a statistical analysis of experimental results
FRIEND_MEAN = RESIL_MEAN = 0.715825523745
FRIEND_STDEV = 0.0426836366557
RESIL_STDEV = 0.130921998163

class TaskSet:
    """Description String"""

    def __init__(self, setUtil, utilMin, utilMax, periodMin, periodMax, rMin, rMax, fMin, fMax, epsilon):
        """Creates taskSet made of SmartTasks"""
        self.setUtil = setUtil
        self.utilMin = utilMin
        self.utilMax = utilMax
        self.periodMin = periodMin
        self.periodMax = periodMax
        self.rMin = rMin
        self.rMax = rMax
        self.fMin = fMin
        self.fMax = fMax
        self.epsilon = epsilon
        self.allTasks = []
        self.partitionList = [None] * 10

        # create tasks, but don't set s_{i:j} values yet
        self.totalUtil = 0
        permID = 0
        while self.totalUtil < setUtil:
            # create task
            util = random() * (utilMax - utilMin) + utilMin
            period = random() * (periodMax - periodMin) + periodMin

            friend = gauss(FRIEND_MEAN, FRIEND_STDEV)
            resil = gauss(RESIL_MEAN, RESIL_STDEV)
            #friend = random() * (self.fMax - self.fMin) + self.fMin
            #resil = random() * (self.rMax - self.rMin) + self.rMin
            self.allTasks.append(SmartTask(util, period, friend, resil, permID))
            self.totalUtil = self.totalUtil + util
            # print(permID)
            # print(self.allTasks[permID])
            # update total util
            permID = permID + 1
        nTotal = permID

        # assign sym values
        for i in range(0, nTotal):
            task = self.allTasks[i]
            task.symRaw = []
            task.symAdj = []
            for j in range(0, nTotal):
                #task.symRaw.append(task.resil * self.allTasks[j].friend + (random() * 2 * epsilon - epsilon))
                task.symRaw.append((task.resil + self.allTasks[j].friend) / 2.0)
                if i==j:
                    task.symAdj.append(1)
                elif task.symRaw[j] <= 0:
                    task.symAdj.append(FAKE_ZERO)
                elif task.symRaw[j] > 1:
                    task.symAdj.append(1)
                else:
                    task.symAdj.append(task.symRaw[j])
            # print(task)


    def addTask(self):
        nTotal=permID=len(self.allTasks)
        util = random() * (self.utilMax - self.utilMin) + self.utilMin
        period = random() * (self.periodMax - self.periodMin) + self.periodMin
        friend = gauss(FRIEND_MEAN, FRIEND_STDEV)
        resil = gauss(RESIL_MEAN, RESIL_STDEV)
        #friend = random() * (self.fMax - self.fMin) + self.fMin
        #resil = random() * (self.rMax - self.rMin) + self.rMin
        self.allTasks.append(SmartTask(util, period, friend, resil, permID))
        self.totalUtil = self.totalUtil + util
        #set sym values for new task
        task=self.allTasks[permID]
        nTotal=nTotal+1
        task.symRaw = []
        task.symAdj = []
        for j in range(0, nTotal):
            #task.symRaw.append(task.resil * self.allTasks[j].friend + (random() * 2 * self.epsilon - self.epsilon))
            task.symRaw.append((task.resil + self.allTasks[j].friend) / 2.0)
            if permID == j:
                task.symAdj.append(1)
            elif task.symRaw[j] <= 0:
                task.symAdj.append(FAKE_ZERO)
            elif task.symRaw[j] > 1:
                task.symAdj.append(1)
            else:
                task.symAdj.append(task.symRaw[j])
        #update sym values for existing tasks
        for j in range(0, nTotal):
            old=self.allTasks[j]
            #old.symRaw.append(old.resil * task.friend + (random() * 2 * self.epsilon -self.epsilon))
            old.symRaw.append((old.resil + task.friend) / 2.0)
            if old.symRaw[permID]<=0:
                old.symAdj.append(FAKE_ZERO)
            elif old.symRaw[permID]>1:
               old.symAdj.append(1)
            else:
                old.symAdj.append(old.symRaw[permID])



    def partitionTasks(self, method):
        """Creates a partition of all tasks in set.  Original tasks are not altered."""
        self.partitionList[method] = Partition(self.allTasks, method)


class Partition:
    ALL_PHYS = 0 # Off
    OBLIVIOUS = 1 
    AWARE_START_THREAD = 2
    AWARE_START_PHYS = 3
    AWARE_START_OBLIV = 4
    OPTIMAL = 5 # Output, but always 0 unless configured
    ALL_THREAD = 6 # Off
    OBLIVIOUS_PLUS = 7 # Off
    #MAX_LOOPS = len(someTasks)

    def __init__(self, someTasks, method):
        self.MAX_LOOPS=len(someTasks)
        self.threadedTasks = {}
        self.physTasks = {}
        if method == Partition.ALL_THREAD:
            for task in someTasks:
                parTask = PartitionedTask(task)
                parTask.threadUtil = task.util / min(task.symAdj)
                self.threadedTasks[task.permID] = parTask
                # print(parTask)
        elif method == Partition.ALL_PHYS:
            self.allPhysical(someTasks)
        elif method == Partition.OBLIVIOUS:
            self.oblivious(someTasks)
        elif method == Partition.OBLIVIOUS_PLUS:
            self.oblivious(someTasks)
            self.updateThreadedUtil(someTasks)
        elif method == Partition.AWARE_START_PHYS:
            self.allPhysical(someTasks)
            self.threadBestPhysPair(someTasks)
            self.updateThreadedUtil(someTasks)
            self.greedyMin(self.MAX_LOOPS, someTasks)
        elif method == Partition.AWARE_START_THREAD:
            # start with tasks threaded unless oblivious threaded util>1
            for task in someTasks:
                parTask = PartitionedTask(task)
                tempThreadUtil = task.util / min(task.symAdj)
                if tempThreadUtil <= 1:
                    parTask.threadUtil = tempThreadUtil
                    self.threadedTasks[task.permID] = parTask
                else:
                    self.physTasks[task.permID] = parTask
                # print ("testing", parTask)
            if len(self.threadedTasks) == 1:
                #print("Only one threaded task.  Reverting to physical.")
                self.allPhysical(someTasks)
            self.updateThreadedUtil(someTasks)
            self.greedyMin(self.MAX_LOOPS, someTasks)
        elif method == Partition.AWARE_START_OBLIV:
            self.oblivious(someTasks)
            self.updateThreadedUtil(someTasks)
            self.greedyMin(self.MAX_LOOPS, someTasks)
        elif method == Partition.OPTIMAL:
            self.optimalPartition(someTasks)
        else:
            print("Invalid partition method.  Default to all physical.")
            self.allPhysical(someTasks)
        # find total thread util and total phys util
        self.totalPhysUtil = 0
        self.totalThreadUtil = 0
        for p in self.physTasks:
            task = self.physTasks[p]
            self.totalPhysUtil = self.totalPhysUtil + task.util
            if task.util > 1: print("Warning: physUtil>1")
        for t in self.threadedTasks:
            task = self.threadedTasks[t]
            self.totalThreadUtil = self.totalThreadUtil + task.threadUtil
            if task.threadUtil > 1:
                print("Warning: threadUtil>1")
            if task.threadUtil < 0:
                print("Warning: threadUtil<0")
        self.coresNeededNoShared();
        self.coresNeededShared();

    def coresNeededNoShared(self):
        self.coresNeededNoShared = np.ceil(self.totalPhysUtil) + np.ceil(self.totalThreadUtil / 2)

    def testUmaFunk(self, m):
        uEffective=self.totalPhysUtil+.5*self.totalThreadUtil
        if uEffective>m:
            return (0, 0)
        #assume we set minimum pi^p; don't need to test
        mh=np.floor(uEffective-self.totalPhysUtil)
        ah = 1 - (self.totalPhysUtil - np.floor(self.totalPhysUtil))
        #sort threaded utilizations
        threadedUtilList=[]
        for t in self.threadedTasks:
            threadedUtilList.append(self.threadedTasks[t].threadUtil)
        threadedUtilList.sort()
        nh = len(threadedUtilList)
        # add some zeros to list if its too short
        while nh < 2 * (mh + 1):
            threadedUtilList.append(0)
            nh = nh + 1
            # largest 2mh+1 items in list
            #note sum is exclusive of last index
        sum1 = sum(threadedUtilList[0:int(2 * mh + 1)])
        if sum1<2*mh or sum1<2*(mh+ah)-threadedUtilList[0]:
            Uma=1
        else:
            Uma=0
        sum2 = sum1 + threadedUtilList[int(2 * mh + 1)]
        if sum1 <= 2 * mh + ah and sum2 <= 2 * (mh + ah):
            Funk=1
        else:
            Funk=0
        return(Uma, Funk)

    def coresNeededShared(self):
        threadedUtilList = []
        uEffective = self.totalPhysUtil + .5 * self.totalThreadUtil
        #print("Phys util:", self.totalPhysUtil)
        #print("Thread util:", self.totalThreadUtil)
        #print("Effective util: ", uEffective)
        # schedulable with uEffective cores?
        m = np.ceil(uEffective)
        mh = np.floor(m - self.totalPhysUtil)
        ah = 1 - (self.totalPhysUtil - np.floor(self.totalPhysUtil))
        # get sorted threaded utilizations
        for t in self.threadedTasks:
            threadedUtilList.append(self.threadedTasks[t].threadUtil)
        threadedUtilList.sort()
        nh = len(threadedUtilList)
        # add some zeros to list if its too short
        while nh < 2 * (mh + 1):
            threadedUtilList.append(0)
            nh = nh + 1
        # largest 2mh+1 items in list
        sum1 = sum(threadedUtilList[0:int(2 * mh + 1)])
        sum2 = sum1 + threadedUtilList[int(2 * mh + 1)]
        if sum1 <= 2 * mh + ah and sum2 < 2 * (mh + ah):
            self.coresNeededShared = m
        else:
            self.coresNeededShared = m + 1

    def allPhysical(self, someTasks):
        self.threadedTasks = {}
        self.physTasks = {}
        for task in someTasks:
            parTask = PartitionedTask(task)
            self.physTasks[task.permID] = parTask

    def oblivious(self, someTasks):
        for task in someTasks:
            parTask = PartitionedTask(task)
            tempThreadUtil = task.util / min(task.symAdj)
            if tempThreadUtil < 1 and task.util / tempThreadUtil >= .5:
                parTask.threadUtil = tempThreadUtil
                self.threadedTasks[task.permID] = parTask
            else:
                self.physTasks[task.permID] = parTask
        if len(self.threadedTasks) == 1:
            # revert to all physical
            #print("Only one threaded task.  Reverting to all tasks physical.")
            self.allPhysical(someTasks)

    def updateThreadedUtil(self, someTasks):
        for i in self.threadedTasks:
            task = someTasks[i]
            minS = 1
            for j in self.threadedTasks:  # requires that partition belong to a task set
                if task.symAdj[j] < minS:
                    minS = task.symAdj[j]
            self.threadedTasks[i].threadUtil = someTasks[i].util / minS

    def threadBestPhysPair(self, someTasks):
        maxDecrease = -1
        #if len(self.threadedTasks) > 0:
            #("Caution: attempting to find best phys pair with pre-existing threaded.")
        for p1 in self.physTasks:
            for p2 in range(p1 + 1, len(self.physTasks) - 1):
                decreaseP1 = self.physTasks[p1].util - .5 * someTasks[p1].util / someTasks[p1].symAdj[p2]
                decreaseP2 = self.physTasks[p2].util - .5 * someTasks[p2].util / someTasks[p1].symAdj[p2]
                totalDecrease = decreaseP1 + decreaseP2
                if totalDecrease > maxDecrease \
                        and someTasks[p1].util / someTasks[p1].symAdj[p2] < 1 \
                        and someTasks[p2].util / someTasks[p2].symAdj[p1] < 1:
                    maxDecrease = totalDecrease
                    bestP1 = p1
                    bestP2 = p2
        if maxDecrease > 0:
            self.threadedTasks[bestP1] = self.physTasks.pop(bestP1)
            self.threadedTasks[bestP1].threadUtil = someTasks[bestP1].util / someTasks[bestP1].symAdj[bestP2]
            self.threadedTasks[bestP2] = self.physTasks.pop(bestP2)
            self.threadedTasks[bestP2].threadUtil = someTasks[bestP2].util / someTasks[bestP2].symAdj[bestP1]
        #else:
            #print("No pair of physTasks could be threaded.")

    def greedyMin(self, maxLoops, someTasks):
        # indicies for tuples returned by picking methods
        WHAT_TASK = 0
        IMPROVEMENT = 1
        for i in range(1, maxLoops):
            # optional: test for feasibility and stop if feasible
            if len(self.threadedTasks) > 1:
                bestPhys = self.pickBestPhysToThread2(someTasks)
            else:
                break
            if len(self.threadedTasks) > 2:
                bestThread = self.pickBestThreadToPhys(someTasks)
            else:
                # don't want to move any threaded task to physical
                bestThread = (-1, -1)
            if bestPhys[IMPROVEMENT] > bestThread[IMPROVEMENT] and bestPhys[IMPROVEMENT] > 0:
                # update threaded utilization values
                taskIndex = bestPhys[WHAT_TASK]
                makeThreaded = someTasks[taskIndex]
                self.physTasks[taskIndex].threadUtil = -1
                for t in self.threadedTasks:
                    if makeThreaded.util / makeThreaded.symAdj[t] > self.physTasks[taskIndex].threadUtil:
                        self.physTasks[taskIndex].threadUtil = makeThreaded.util / makeThreaded.symAdj[t]
                    if self.threadedTasks[t].threadUtil < someTasks[t].util / someTasks[t].symAdj[taskIndex]:
                        self.threadedTasks[t].threadUtil = someTasks[t].util / someTasks[t].symAdj[taskIndex]
                # remove bestPhys from physIn and add to threadIn
                self.threadedTasks[taskIndex] = self.physTasks.pop(taskIndex)
                # print("Moving", taskIndex, "to threaded.")
            elif bestThread[IMPROVEMENT] > 0:
                # update utilizations of remaining threaded tasks
                # if bestThread was the worst for some other threaded tasks, reduce that task's util
                t1 = bestThread[WHAT_TASK]
                for t2 in self.threadedTasks:
                    # if t1 is the worst for t2 among currently threaded tasks
                    if self.threadedTasks[t2].threadUtil == someTasks[t2].util / someTasks[t2].symAdj[t1]:
                        # find new threadUtil for t2
                        self.threadedTasks[t2].threadUtil = 0
                        for t3 in self.threadedTasks:
                            if t3 != t2 and t3 != t1:
                                if someTasks[t2].util / someTasks[t2].symAdj[t3] > self.threadedTasks[t2].threadUtil:
                                    self.threadedTasks[t2].threadUtil = someTasks[t2].util / someTasks[t2].symAdj[t3]
                    # else t1 is NOT worst-case for t2, so t2 does not get to reduce its threadUtil
                # move bestThread to phys
                self.threadedTasks[t1].threadUtil = -1
                self.physTasks[t1] = self.threadedTasks.pop(t1)
                # print("Moving", t1, "to physical.")
            else:
                # move random theaded task to phys?
                #print("Tasks moved:", i)
                break  # no improvement possible; need to quit

    def greedyMin2(self, maxLoops, someTasks):
        WHAT_TASK = 0
        IMPROVEMENT = 1
        for i in range(1, maxLoops):
            if len(self.threadedTasks) > 1:
                bestPhysToThread = self.pickBestPhysToThread2(someTasks)
            else:
                break
            if bestPhysToThread[IMPROVEMENT] > 0:
                moveToThread = bestPhysToThread[WHAT_TASK]
                for t in self.threadedTasks:
                    if someTasks[moveToThread].util / someTasks[moveToThread].symAdj[t] > self.physTasks[
                        moveToThread].threadUtil:
                        self.physTasks[moveToThread].threadUtil = someTasks[moveToThread].util / \
                                                                  someTasks[moveToThread].symAdj[t]
                    if self.threadedTasks[t].threadUtil > someTasks[t].util / someTasks[t].symAdj[moveToThread]:
                        self.threadedTasks[t].threadUtil = someTasks[t].util / someTasks[t].symAdj[moveToThread]
                self.threadedTasks[moveToThread] = self.physTasks.pop(moveToThread)
            else:
                break
        #print("Tasks moved", i)

    def pickBestPhysToThread2(self, someTasks):
        maxDecrease = -1
        bestP = -1
        for p in self.physTasks:
            skip = False
            candidate = someTasks[p]
            physUtil = candidate.util
            utilIfThread = 0
            increaseToThreaded = 0
            for t in self.threadedTasks:
                temp = physUtil / candidate.symAdj[t]
                if temp > 1:
                    skip = True
                    # t=-1
                    break
                if temp > utilIfThread:
                    utilIfThread = temp
                temp = someTasks[t].util / someTasks[t].symAdj[p]
                if temp > 1:
                    skip = True
                    # t=-1
                    break
                if temp > self.threadedTasks[t].threadUtil:
                    increaseToThreaded = increaseToThreaded + temp - self.threadedTasks[t].threadUtil
            if skip:
                continue
            totalDecrease = physUtil - .5 * (utilIfThread + increaseToThreaded)
            if totalDecrease > maxDecrease:
                bestP = p
                maxDecrease = totalDecrease
        return bestP, maxDecrease

    def pickBestPhysToThread(self, someTasks):
        bestP = -1
        maxImprovement = 0
        decreaseUtil = {}
        for p in self.physTasks:
            tempThreadUtil = 0
            decreaseUtil[p] = 0
            skip = False
            for t in self.threadedTasks:
                # what happens to p if we move it to threaded?
                if tempThreadUtil < someTasks[p].util / someTasks[p].symAdj[t]:
                    tempThreadUtil = someTasks[p].util / someTasks[p].symAdj[t]
                    if tempThreadUtil > 1:
                        skip = True
                        #print("Moving", p, "to threaded would give", p, "util>1.")
                        break
                # what happens to already threaded tasks if we move p to threaded?
                newUtil = someTasks[t].util / someTasks[t].symAdj[p]
                if newUtil > 1:
                    skip = True
                    #print("Moving", p, "to threaded would give", t, "util>1.")
                    break
                if self.threadedTasks[t].threadUtil < newUtil:
                    decreaseUtil[p] = decreaseUtil[p] - .5 * (newUtil - self.threadedTasks[t].threadUtil)
            if skip: continue
            decreaseUtil[p] = decreaseUtil[p] - .5 * tempThreadUtil + someTasks[p].util
            if decreaseUtil[p] > maxImprovement:
                maxImprovement = decreaseUtil[p]
                bestP = p
                # print ("bestP=", bestP)
        return bestP, maxImprovement

    def pickBestThreadToPhys(self, someTasks):
        # assumes that at least three tasks are threaded
        for t1 in self.threadedTasks:
            maxImprovement = -2
            bestT = -1
            increaseThisTask = someTasks[t1].util - self.threadedTasks[t1].threadUtil / 2
            decreaseOtherTasks = 0
            for t2 in self.threadedTasks:
                # if t1 is the worst for t2 among currently threaded tasks
                if self.threadedTasks[t2].threadUtil == someTasks[t2].util / someTasks[t2].symAdj[t1]:
                    # find new threadUtil for t2
                    newThreadUtil = 0
                    for t3 in self.threadedTasks:
                        if t3 != t2 and t3 != t1:
                            if someTasks[t2].util / someTasks[t2].symAdj[t3] > newThreadUtil:
                                newThreadUtil = someTasks[t2].util / someTasks[t2].symAdj[t3]
                    decreaseOtherTasks = decreaseOtherTasks + (self.threadedTasks[t2].threadUtil - newThreadUtil) / 2
                # else t1 is NOT worst-case for t2, so t2 does not get to reduce its threadUtil
            if decreaseOtherTasks - increaseThisTask > maxImprovement:
                maxImprovement = decreaseOtherTasks - increaseThisTask
                bestT = t1
        return bestT, maxImprovement

    def optimalPartition(self, someTasks):
        bestThreaded = {}
        n = len(someTasks)
        utilAllPhys = 0
        for p in someTasks:
            utilAllPhys = utilAllPhys + p.util
        minTEU = utilAllPhys
        # check all partitions with 3 to n-1 threaded tasks, inclusive
        # 2 threaded tasks covered by greedy physStart
        # n threaded tasks covered by greedy threadStart
        for threadCount in range(2, n+1):
            # get set of all partitions that have threadCount threaded tasks
            allThreadedOfSize = itertools.combinations(someTasks, threadCount)
            for threadSet in allThreadedOfSize:
                self.threadedTasks={}
                skip=False
                for t1 in threadSet:
                    index=t1.permID
                    self.threadedTasks[index] = PartitionedTask(someTasks[index])
                    for interfere in threadSet:
                        if self.threadedTasks[index].threadUtil < self.threadedTasks[index].util / someTasks[index].symAdj[
                            interfere.permID]:
                            self.threadedTasks[index].threadUtil = self.threadedTasks[index].util / someTasks[index].symAdj[
                                interfere.permID]
                            if self.threadedTasks[index].threadUtil > 1:
                                skip = True
                                break
                    if skip:
                        break
                if skip:
                    continue
                tempTEU = utilAllPhys
                for t2 in threadSet:
                    tempTEU = tempTEU - someTasks[t2.permID].util + .5 * self.threadedTasks[t2.permID].threadUtil
                if tempTEU < minTEU:
                    minTEU = tempTEU
                    bestThreaded = self.threadedTasks.copy()
        #partition to match the best found
        self.allPhysical(someTasks)
        self.threadedTasks=bestThreaded
        for t in self.threadedTasks:
            del self.physTasks[t]


    def __str__(self):
        physString = " "

        threadString = " "

        for p in self.physTasks:
            physString = physString + str(self.physTasks[p]) + "\n"

        for t in self.threadedTasks:
            threadString = threadString + str(self.threadedTasks[t]) + "\n"

        return physString + threadString


class SmartTask:
    """description string"""

    def __init__(self, util, period, friend, resil, permID):
        self.util = float(util)
        self.period = period
        self.cost = util * period
        self.friend = friend
        self.resil = resil
        self.symRaw = []  # will hold s_{i:j} values for all j; may be >1 or <0
        self.symAdj = []  # all values in range (0, 1]
        self.permID = permID

    def __str__(self):
        strSymAdj = str(self.symAdj)
        return str(str(self.permID) + " " + str(self.util) + " " + strSymAdj)

        # every task needs a unique ID that holds across all partitions


class PartitionedTask:

    def __init__(self, parent):
        self.util = parent.util
        self.period = parent.period
        self.permID = parent.permID
        self.threadUtil = -1  # has no meaning in isolation

    def __str__(self):
        self.status = ""
        self.printUtil = ""
        if self.threadUtil == -1:
            self.status = "phys"
            self.printUtil = str(self.util)
        else:
            self.status = "threaded"
            self.printUtil = str(self.threadUtil)
        return str(str(self.permID) + " " + self.status + " " + self.printUtil)

'''
# def __init__(self, setUtil, utilMin, utilMax, periodMin, periodMax, rMin, rMax, fMin, fMax, epsilon)
myTaskSet = TaskSet(24, .0, .3, 10, 100, .8, 1.1, .8, 1.1, .1)
# print("All Threads")
# myTaskSet.partitionTasks(Partition.ALL_THREAD)
# print (myTaskSet.partitionList[Partition.ALL_THREAD])

print("All Phys")
myTaskSet.partitionTasks(Partition.ALL_PHYS)
# print (myTaskSet.partitionList[Partition.ALL_PHYS])
# print ("noShared=", myTaskSet.partitionList[Partition.ALL_PHYS].coresNeededNoShared)
print("Shared=", myTaskSet.partitionList[Partition.ALL_PHYS].coresNeededShared)
print("")

print("Oblivious")
myTaskSet.partitionTasks(Partition.OBLIVIOUS)
# print (myTaskSet.partitionList[Partition.OBLIVIOUS])
# print ("noShared=", myTaskSet.partitionList[Partition.OBLIVIOUS].coresNeededNoShared)
print("Shared=", myTaskSet.partitionList[Partition.OBLIVIOUS].coresNeededShared)
print("")

print("Oblivious Plus")
myTaskSet.partitionTasks(Partition.OBLIVIOUS_PLUS)
# print (myTaskSet.partitionList[Partition.OBLIVIOUS_PLUS])
# print ("noShared=", myTaskSet.partitionList[Partition.OBLIVIOUS_PLUS].coresNeededNoShared)
print("Shared=", myTaskSet.partitionList[Partition.OBLIVIOUS_PLUS].coresNeededShared)
print("")

print("Aware Start Thread")
myTaskSet.partitionTasks(Partition.AWARE_START_THREAD)
# print (myTaskSet.partitionList[Partition.AWARE_START_THREAD])
# print ("noShared=", myTaskSet.partitionList[Partition.AWARE_START_THREAD].coresNeededNoShared)
print("Shared=", myTaskSet.partitionList[Partition.AWARE_START_THREAD].coresNeededShared)
print("")

print("Aware Start Phys")
myTaskSet.partitionTasks(Partition.AWARE_START_PHYS)
# print (myTaskSet.partitionList[Partition.AWARE_START_PHYS])
# print ("noShared=", myTaskSet.partitionList[Partition.AWARE_START_PHYS].coresNeededNoShared)
print("Shared=", myTaskSet.partitionList[Partition.AWARE_START_PHYS].coresNeededShared)
print("")

print("Aware Start Obliv")
myTaskSet.partitionTasks(Partition.AWARE_START_OBLIV)
# print (myTaskSet.partitionList[Partition.AWARE_START_OBLIV])
# print ("noShared=", myTaskSet.partitionList[Partition.AWARE_START_OBLIV].coresNeededNoShared)
print("Shared=", myTaskSet.partitionList[Partition.AWARE_START_OBLIV].coresNeededShared)
print("")

#print("Optimal")
#myTaskSet.partitionTasks(Partition.OPTIMAL)
#print (myTaskSet.partitionList[Partition.OPTIMAL])
# print ("noShared=", myTaskSet.partitionList[Partition.AWARE_START_OBLIV].coresNeededNoShared)
#print("Shared=", myTaskSet.partitionList[Partition.OPTIMAL].coresNeededShared)
print("")
'''
