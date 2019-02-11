#!/usr/bin/env bash
./RunTests.py 4 500 4_500_1_normal.txt &
./RunTests.py 8 500 8_500_1_normal.txt &
./RunTests.py 16 500 16_500_1_normal.txt &
./RunTests.py 32 500 32_500_1_normal.txt &

./RunTests.py 4 500 4_500_1_2_normal.txt 0 1 2 &
./RunTests.py 8 500 8_500_1_2_normal.txt 0 1 2 &
./RunTests.py 16 500 16_500_1_2_normal.txt 0 1 2 &
./RunTests.py 32 500 32_500_1_2_normal.txt 0 1 2 &

./RunTests.py 4 500 4_500_2_1_normal.txt 0 2 1 &
./RunTests.py 8 500 8_500_2_1_normal.txt 0 2 1 &
./RunTests.py 16 500 16_500_2_1_normal.txt 0 2 1 &
./RunTests.py 32 500 32_500_2_1_normal.txt 0 2 1 &

./RunTests.py 4 500 4_500_2_2_normal.txt 0 2 2 &
./RunTests.py 8 500 8_500_2_2_normal.txt 0 2 2 &
./RunTests.py 16 500 16_500_2_2_normal.txt 0 2 2 &
./RunTests.py 32 500 32_500_2_2_normal.txt 0 2 2 &
