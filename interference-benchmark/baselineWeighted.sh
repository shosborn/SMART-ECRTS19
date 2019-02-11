#!/bin/bash

core=$1
baseJobs=$2
runID=$3


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

	#background programs
	#note: C program will loop forever if output==0
	PID_list=""
	for k in {8..15}
	do
		if [ $k -ne $core ]
		then
			rand=$(( $RANDOM % 19 ))
			#taskset -c $k chrt -f 97 ./${tacleProg[$rand]} NA $backgroundLoops NA NA NA NA 0 &
			taskset -c $k chrt -f 96 ./${tacleProg[$rand]} NA $backgroundLoops NA NA NA NA 0 &


			#PID[$k]=$!
			lastPID=$!
			PID_list="$PID_list $lastPID"
	#		echo $lastPID ${tacleProg[$rand]}
		fi
	done

	#echo $PID_list
	
	#echo backgroundRunning

	#primary program
	taskset -c $core chrt -f 97 ./${tacleProg[$i]} ${tacleProg[$i]} $maxJobs $core none none $runID 1 $PID_list	
	#for k in {8..15}
	#do
	#	kill ${PID[$k]}
	#done
	echo ${tacleProg[$i]}
done


