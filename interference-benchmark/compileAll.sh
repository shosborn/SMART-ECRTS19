#!/bin/bash
while read t; do
  gcc /home/shosborn/Documents/sequential/timed/$t/*.c -o /scratch/tacleSeq/$t
done <tacleNames.txt
