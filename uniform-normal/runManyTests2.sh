#!/usr/bin/env bash
mkdir -p results
python3 RunTests.py 4 100 .01 0 results/4_100_01_normal &
python3 RunTests.py 4 100 .055 0 results/4_100_055_normal &
python3 RunTests.py 4 100 .1 0 results/4_100_1_normal &
python3 RunTests.py 8 100 .01 0 results/8_100_01_normal &
python3 RunTests.py 8 100 .055 0 results/8_100_055_normal &
python3 RunTests.py 8 100 .1 0 results/8_100_1_normal &
python3 RunTests.py 16 100 .01 0 results/16_100_01_normal &
python3 RunTests.py 16 100 .055 0 results/16_100_055_normal &
python3 RunTests.py 16 100 .1 0 results/16_100_1_normal &
python3 RunTests.py 32 100 .01 0 results/32_100_01_normal &
python3 RunTests.py 32 100 .055 0 results/32_100_055_normal &
python3 RunTests.py 32 100 .1 0 results/32_100_1_normal &
python3 RunTests.py 4 1000 .01 0 results/4_1000_01_normal &
python3 RunTests.py 4 1000 .055 0 results/4_1000_055_normal &
python3 RunTests.py 4 1000 .1 0 results/4_1000_1_normal &
python3 RunTests.py 8 1000 .01 0 results/8_1000_01_normal &
python3 RunTests.py 8 1000 .055 0 results/8_1000_055_normal &
python3 RunTests.py 8 1000 .1 0 results/8_1000_1_normal &
python3 RunTests.py 16 1000 .01 0 results/16_1000_01_normal &
python3 RunTests.py 16 1000 .055 0 results/16_1000_055_normal &
python3 RunTests.py 16 1000 .1 0 results/16_1000_1_normal &
python3 RunTests.py 32 1000 .01 0 results/32_1000_01_normal &
python3 RunTests.py 32 1000 .055 0 results/32_1000_055_normal &
python3 RunTests.py 32 1000 .1 0 results/32_1000_1_normal &
