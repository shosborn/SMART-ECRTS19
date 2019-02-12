# Schedulability Studies with Gaussian-Average SMT Interference Modeling

## Running

All the `./results` data can be modeled by simply running the following shell scripts:
```
./run_4-32_100_mixed_stdev.sh
./run_4-32_500_mixed_stdev.sh
./run_4-32_1000_mixed_stdev.sh
```
Each will yield a full premuted set of results under 100, 500, or 1000 samples.

## Disambiguation

In `results` 

## Results Guide

- `./1st-run-archive` contains our first run of this benchmark suite with the updated modeling. Contains a large amount of repeated data due to bad permutation management. **DEPRECATED**
- `./results` contains the primary results used in the paper. This models standard deviation multipliers from the sets [1,2] and [2,3] for both `s` and `f`.
