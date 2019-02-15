#!/usr/bin/env bash

# Check that the number of iterations was specified

if [ -z "$1" ]
then
    echo "Usage: $0 <number of iterations>"
    echo "Recommended iterations: between 100 and 1000"
    exit 1
fi

# Setup someplace to store results

mkdir -p results

# All permutations of stdev 1 on s with [1,3] for f

./RunTests.py 4 ${1} results/4_${1}_1_1_normal.txt &
./RunTests.py 8 ${1} results/8_${1}_1_1_normal.txt &
./RunTests.py 16 ${1} results/16_${1}_1_1_normal.txt &
./RunTests.py 32 ${1} results/32_${1}_1_1_normal.txt &

./RunTests.py 4 ${1} results/4_${1}_1_2_normal.txt 0 1 2 &
./RunTests.py 8 ${1} results/8_${1}_1_2_normal.txt 0 1 2 &
./RunTests.py 16 ${1} results/16_${1}_1_2_normal.txt 0 1 2 &
./RunTests.py 32 ${1} results/32_${1}_1_2_normal.txt 0 1 2 &

./RunTests.py 4 ${1} results/4_${1}_1_3_normal.txt 0 1 3 &
./RunTests.py 8 ${1} results/8_${1}_1_3_normal.txt 0 1 3 &
./RunTests.py 16 ${1} results/16_${1}_1_3_normal.txt 0 1 3 &
./RunTests.py 32 ${1} results/32_${1}_1_3_normal.txt 0 1 3 &

# All permutations of stdev 2 on s with [1,3] for f

./RunTests.py 4 ${1} results/4_${1}_2_1_normal.txt 0 2 1 &
./RunTests.py 8 ${1} results/8_${1}_2_1_normal.txt 0 2 1 &
./RunTests.py 16 ${1} results/16_${1}_2_1_normal.txt 0 2 1 &
./RunTests.py 32 ${1} results/32_${1}_2_1_normal.txt 0 2 1 &

./RunTests.py 4 ${1} results/4_${1}_2_2_normal.txt 0 2 2 &
./RunTests.py 8 ${1} results/8_${1}_2_2_normal.txt 0 2 2 &
./RunTests.py 16 ${1} results/16_${1}_2_2_normal.txt 0 2 2 &
./RunTests.py 32 ${1} results/32_${1}_2_2_normal.txt 0 2 2 &

./RunTests.py 4 ${1} results/4_${1}_2_3_normal.txt 0 2 3 &
./RunTests.py 8 ${1} results/8_${1}_2_3_normal.txt 0 2 3 &
./RunTests.py 16 ${1} results/16_${1}_2_3_normal.txt 0 2 3 &
./RunTests.py 32 ${1} results/32_${1}_2_3_normal.txt 0 2 3 &

# All permutations of stdev 3 on s with [1,3] for f

./RunTests.py 4 ${1} results/4_${1}_3_1_normal.txt 0 3 1 &
./RunTests.py 8 ${1} results/8_${1}_3_1_normal.txt 0 3 1 &
./RunTests.py 16 ${1} results/16_${1}_3_1_normal.txt 0 3 1 &
./RunTests.py 32 ${1} results/32_${1}_3_1_normal.txt 0 3 1 &

./RunTests.py 4 ${1} results/4_${1}_3_2_normal.txt 0 3 2 &
./RunTests.py 8 ${1} results/8_${1}_3_2_normal.txt 0 3 2 &
./RunTests.py 16 ${1} results/16_${1}_3_2_normal.txt 0 3 2 &
./RunTests.py 32 ${1} results/32_${1}_3_2_normal.txt 0 3 2 &

./RunTests.py 4 ${1} results/4_${1}_3_3_normal.txt 0 3 3 &
./RunTests.py 8 ${1} results/8_${1}_3_3_normal.txt 0 3 3 &
./RunTests.py 16 ${1} results/16_${1}_3_3_normal.txt 0 3 3 &
./RunTests.py 32 ${1} results/32_${1}_3_3_normal.txt 0 3 3 &
