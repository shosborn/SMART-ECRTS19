## Interference Benchmarks/Modified TACLeBench

Most changes are constrained to `./benchmarks/extra.h`.

Run `./baselineWeighted.sh` and `./allPairsWeighted.sh` to execute benchmarks and determine the all-pairs performance degradation under SMT for TACLeBench.

Our benchmark results used for the paper are in the `./results` directory and summarized in `./results/MoonlightData6.xlsx`.

Based off [the original TACLe benchmark collection](https://github.com/tacle/tacle-bench).

## Analysis

Running `python3 ./summarize.py <results file>` will summarize the test data from a specified results file. This data can then be loaded into supplemental analysis as demonstrated in `./results/MoonlightData6.xlxs` to derive the results from the paper.
