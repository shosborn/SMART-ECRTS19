#!/bin/bash

firstCore=$1
secondCore=$2
baseJobs=$3
runID=$4


#turn off rt throttling
echo -1 >/proc/sys/kernel/sched_rt_runtime_us

j=0
while read i; do
	tacleProg[$j]=$i
	j=$(( $j + 1 ))
done <tacleNames.txt

j=0

for i in {0..18}
do
	#shorter jobs get more loops
	thisProg=${tacleProg[$i]}
	if [ "$thisProg" = "petrinet" -o "$thisProg" = "statemate" ]
	then
		maxJobs=`expr $baseJobs \* 100`
	elif [ "$thisProg" = "cjpeg_wrbmp" -o "$thisProg" = "fmref" -o "$thisProg" = "h264_dec" -o "$thisProg" = "ndes" ]
	then
		maxJobs=`expr $baseJobs \* 10`
	elif  [ "$thisProg" = "adpcm_dec" -o "$thisProg" = "adpcm_enc" -o "$thisProg" = "cjpeg_transupp" -o "$thisProg" = "epic" -o "$thisProg" = "gsm_dec" -o "$thisProg" = "huff_enc" -o "$thisProg" = "rijndael_dec" -o "$thisProg" = "rijndael_enc" ]
	then
		maxJobs=`expr $baseJobs \* 1`
	else
		maxJobs=$baseJobs
	fi

	backgroundLoops=`expr $maxJobs \* 10000000`
	
	#echo $backgroundLoops

	for j in {0..18} #loop through programs
	do
		#secondary program
		taskset -c $secondCore chrt -f 97 ./${tacleProg[$j]} NA $backgroundLoops NA NA NA NA 0 &
		lastPID=$!
		#PID_list="$PID_list $lastPID"		
		PID_list="$lastPID"

		#primary program
		taskset -c $firstCore chrt -f 97 ./${tacleProg[$i]} ${tacleProg[$i]} $maxJobs $firstCore $secondCore ${tacleProg[$j]} $runID 1 $PID_list
		
		if [ $j -eq $i ]
		then	
			echo ${tacleProg[$i]}
		fi
	done
done

