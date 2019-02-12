# Schedulability Studies with Uniform-Normal SMT Interference Modeling

This subdirectory contains the python code needed to model the schedulability
of tasks systems with strength and friendliness scores chosen with the uniform-
normal method. Our raw data is also available in `./results`. (Note that this
is largely similar to the code used for the Gaussian-average studies.)

## Running

All the `./results` data used in the paper can be modeled by simply running
`./runManyTests2.sh`. **Warning:** on a moderately recent 24-core Intel Xeon-
based server these experiments take about a week to run. Editing the
execution script to exclude higher-core-count CPUs will substantially improve
the runtime if you are uninterested in those platforms.

## Results Guide

We model systems with 4, 8, 16, and 32 cores under all permutations of the
utilization range settings (0, .4], [.3, .7], (0, 1), strength and friendliness
ranges (independently) [.65, 1], [.7, 1], [.75, 1], [.8, 1], and epsilons 0.55,
0.1, and 1. Please see our paper for further detail.

## Titling Disambiguation

In `./results`, each file is titled in the format
`<core count>_<iteration count>_<epsilon>_normal.txt` where angle brackets
represent substitutions.

