#!/usr/bin/env bash
./RunTests.py 4 100 /playpen/jbakita/4_100_1_normal.txt &
./RunTests.py 8 100 /playpen/jbakita/8_100_1_normal.txt &
./RunTests.py 16 100 /playpen/jbakita/16_100_1_normal.txt &
./RunTests.py 32 100 /playpen/jbakita/32_100_1_normal.txt &

./RunTests.py 4 100 /playpen/jbakita/4_100_1_2_normal.txt 0 1 2 &
./RunTests.py 8 100 /playpen/jbakita/8_100_1_2_normal.txt 0 1 2 &
./RunTests.py 16 100 /playpen/jbakita/16_100_1_2_normal.txt 0 1 2 &
./RunTests.py 32 100 /playpen/jbakita/32_100_1_2_normal.txt 0 1 2 &

./RunTests.py 4 100 /playpen/jbakita/4_100_2_1_normal.txt 0 2 1 &
./RunTests.py 8 100 /playpen/jbakita/8_100_2_1_normal.txt 0 2 1 &
./RunTests.py 16 100 /playpen/jbakita/16_100_2_1_normal.txt 0 2 1 &
./RunTests.py 32 100 /playpen/jbakita/32_100_2_1_normal.txt 0 2 1 &

./RunTests.py 4 100 /playpen/jbakita/4_100_2_2_normal.txt 0 2 2 &
./RunTests.py 8 100 /playpen/jbakita/8_100_2_2_normal.txt 0 2 2 &
./RunTests.py 16 100 /playpen/jbakita/16_100_2_2_normal.txt 0 2 2 &
./RunTests.py 32 100 /playpen/jbakita/32_100_2_2_normal.txt 0 2 2 &
