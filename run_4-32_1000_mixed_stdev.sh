#!/usr/bin/env bash
./RunTests.py 4 1000 4_1000_1_normal.txt &
./RunTests.py 8 1000 8_1000_1_normal.txt &
./RunTests.py 16 1000 16_1000_1_normal.txt &
./RunTests.py 32 1000 32_1000_1_normal.txt &

./RunTests.py 4 1000 4_1000_1_2_normal.txt 0 1 2 &
./RunTests.py 8 1000 8_1000_1_2_normal.txt 0 1 2 &
./RunTests.py 16 1000 16_1000_1_2_normal.txt 0 1 2 &
./RunTests.py 32 1000 32_1000_1_2_normal.txt 0 1 2 &

./RunTests.py 4 1000 4_1000_2_1_normal.txt 0 2 1 &
./RunTests.py 8 1000 8_1000_2_1_normal.txt 0 2 1 &
./RunTests.py 16 1000 16_1000_2_1_normal.txt 0 2 1 &
./RunTests.py 32 1000 32_1000_2_1_normal.txt 0 2 1 &

./RunTests.py 4 1000 4_1000_2_2_normal.txt 0 2 2 &
./RunTests.py 8 1000 8_1000_2_2_normal.txt 0 2 2 &
./RunTests.py 16 1000 16_1000_2_2_normal.txt 0 2 2 &
./RunTests.py 32 1000 32_1000_2_2_normal.txt 0 2 2 &
