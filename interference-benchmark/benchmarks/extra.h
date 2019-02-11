#include <time.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <limits.h>

#define L3_CACHE_SIZE (11264*1024)

#define SAVE_RESULTS if(jobsComplete>-1) progTime[jobsComplete]=(end.tv_nsec-start.tv_nsec)+(1000000000*(end.tv_sec-start.tv_sec));


#define SET_UP char *thisProgram=argv[1];\
	int maxJobs=atoi(argv[2]);\
        char *thisCore=argv[3];\
        char *otherCore=argv[4];\
        char *otherProgram=argv[5];\
        char *runID=argv[6];\
	int output=atoi(argv[7]);\
	int firstPID_index=8;\
	int curPID_index;\
	pid_t killMe;\
	struct timespec start, end;\
	int jobsComplete;\
	long progTime[maxJobs*output];\
	char fileName[50];\
	char *bigArray;\
	int wasteCount;\
	strcpy(fileName, runID);\
	strcat(fileName, ".txt");\
	mlockall(MCL_CURRENT || MCL_FUTURE);


#define KILL_OTHERS for (curPID_index=firstPID_index; curPID_index<argc; curPID_index++){\
	killMe=(pid_t) atoi(argv[curPID_index]);\
	kill (killMe, SIGKILL);}
	

//	if (otherPID>0) kill(otherPID, SIGKILL);\

//if output==0, endless loop
//avoids int overflow error with large numbers for background loops

#define WRITE_TO_FILE if (output){\
	munlockall();\
	KILL_OTHERS\
	FILE *fp=fopen(fileName, "a");\
	for(jobsComplete=0; jobsComplete<maxJobs; jobsComplete++){\
		fprintf(fp, "%s %s %s %s %d %ld %s %d \n",\
		thisProgram, otherProgram, thisCore, otherCore, maxJobs,\
		progTime[jobsComplete], runID, jobsComplete);\
	}\
	fclose(fp);\
	}

#define KILL_CACHE bigArray=(char *)malloc(L3_CACHE_SIZE);\
if (bigArray==NULL) perror("Malloc failed.\n");\
memset(bigArray, 1, L3_CACHE_SIZE);\
munlock(bigArray, L3_CACHE_SIZE);\
free(bigArray);\
bigArray=NULL;



//invoke start timer twice, stop timer to make sure timer and vars are in cache
#define START_TIMER clock_gettime(CLOCK_MONOTONIC, &start);\
        clock_gettime(CLOCK_MONOTONIC, &end);\
	clock_gettime(CLOCK_MONOTONIC, &start);\
		
#define STOP_TIMER clock_gettime(CLOCK_MONOTONIC, &end);


//waste a millisecond

#define WASTE_TIME clock_gettime(CLOCK_MONOTONIC, &start);\
do{clock_gettime(CLOCK_MONOTONIC, &end);}\
while( (end.tv_sec*1000000000+end.tv_nsec)-(start.tv_sec*1000000000+start.tv_nsec) < 1000000);


#define SLEEP nanosleep((const struct timespec[]){{0, 1000000}}, NULL);

//#define LOOP_WASTE for(wasteCount=0; wasteCount<1000000; wasteCount++){}

//at beginning of loop clear cache, waste some time
//wasting time allows interfering process to build up some cache presence
//using sleep instead of waste time loop causes problems
//both sleeping and spinning give advantage to threaded task
#define START_LOOP if (output) {KILL_CACHE  START_TIMER}

#define STOP_LOOP if (output) {STOP_TIMER SAVE_RESULTS}
//if (!output) {jobsComplete--;}


/*
Intended structure

main
SET_UP
notice that STOP LOOP negates the ++ if outout=0
for (jobsComplete=-1; jobsComplete<maxJobs; jobsComplete++){
		KILL_CACHE
		START_TIMER
		tacleInit();
		tacleMain();
		STOP_TIMER
		SAVE_RESULTS
}
WRITE_TO_FILE
tacleReturn	
*/
