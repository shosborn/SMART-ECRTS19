# Schedulability Study and SMART-Interference Measurement Code

This repository contains the code to execute the schedulability studies and experiments for the ECRTS'19 submission, "Simultaneous Multithreading Applied to Real Time" by Sims Hill Osborne, Joshua J. Bakita, and James H. Anderson. We also include our experimental results.

## Overview

Each folder in this repository corresponds to one of our code bases and seperately contains help files
- `/interference-benchmark` contains our version of TACLeBench modified to measure SMT interference costs and contains our results from those experiments
- `/gaussian-average` contains our schedulability study code and results from when using the _gaussian-average_ inter-task interference model
- `/uniform-normal` contains our schedulability study code and results from when using the _uniform-normal_ inter-task interference model
