# Schedulability Studies with Gaussian-Average SMT Interference Modeling

## Running

All the `./results` data used in the paper can be modeled by simply running
`./run_4-32_mixed_stdev.sh 1000`. The other, lower resolution test data can
be reproduced by running the same script with a lower sample count (i.e.
100 or 500 rather than 1000).

## Results Guide

- `./results` contains the primary results used in the paper. This models
  standard deviation multipliers from the sets [1,3] for both strength and
  friendliness. Utilization windows are (0, 1), (0, 0.4], [0.3, 0.7], and
  [0.6, 1) with periods inside the window [10, 100].
- `./1st-run-archive` contains our first run of this benchmark suite with the
  updated modeling. Contains a large amount of repeated data due to bad
  permutation management. **DEPRECATE:D** Not used in the paper and simply
  stored here for archival purposes.

## Titling Disambiguation

In `./results`, each file is titled in the format
`<core count>_<iteration count>_<strength standard deviation multiplier>_<friendliness standard deviation multiplier>_normal.txt`
where angle brackets represent substitutions.

## Data Format

Each result file contains four runs (one for each of the four utilization
ranges). The beginning of one of these runs is indicated by a single line
containing `*****`. The immediately following header line indicates the setting
on each of the test variables in the format
`<core count>_<bin size>_<iteration count>_<lower utilization bound>_<upper utilization bound>_<lower period bound>_<upper period bound>_<strength standard deviation>_<friendliness standard deviation>`.
The following lines each indicate the aggregate results from a test utilization
bin in the format:
`<lower bound of utilization bin>,<total tasks>,<tasks schedulable with Oblivious>,<tasks schedulable with Greedy-Thread>,<tasks schedulable with Greedy-Physical>,<tasks schedulable with Greedy-Mixed>,0,0,0,0,0,0`.
