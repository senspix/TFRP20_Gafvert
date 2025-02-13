# Assignment 2

## TODO #1: Understanding the given models and viewer tool
Install seaborn dependency:
```
conda install -c conda-forge seaborn
```
## TODO #2: Implementation
**Implement** a localisation / tracking approach based on an HMM with a) simple **Forward Filtering**
and b) **Forward-Backward Smoothing** with k = t-5 (a sequence length of 5) to track the robot
(according to the matrix-vector notation suggested in section 14.3.1 of the course book and the
respective lecture material, i.e. make use of the given models!).
This requires obviously a two-part implementation, as you first need to “simulate the robot” with its
movement a) to have some ground truth to evaluate your tracking against, and b) to simulate a
sensor reading from this robot for the HMM-based tracking algorithm.
**You must make use of the given models for the robot simulation and the filtering / smoothing!**

Your algorithm should basically loop over the following three steps, where steps 2 and 3 can have
several instances for the comparing evaluations:
1. Move (simulated) robot to new pose using move_once(…) in RobotSim.py;
2. obtain (simulated) sensor reading(s) using sense_in_current_state(…), with the
observation model you want to use. Note that it is possible to call
sense_in_current_state(…) as often as you like with different observation model
instances, getting a sensor reading will not affect the true pose;
3. update the position estimate with either the forward- or smoothing approach based on
the sensor reading(s) from step 2, using the known observation and transition models in
your implementations of the forward filter and smoothing algorithms.
Note that a sensor reading of “nothing” normally means to do the forward step without
update, i.e. it boils down to mere prediction in theory. However, here, you should not go the
normal way, but always do a complete update.
Thus, even a “nothing” reading from the sensor should entail a proper prediction +
update step!

## TODO #3: Evaluation
## TODO #4: Peer review
## TODO #5: Reading article
## TODO #6: Writing report
