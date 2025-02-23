from models import *
from Filters import HMMFilter, HMMSmoother

import numpy as np
import matplotlib.pyplot as plt
import random


def manhattan_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])



HEADINGS = ['S', 'E', 'N', 'W']
POSE_ROW = 0
POSE_COL = 1
POSE_HEAD = 2


def estimate_position(f, sm):
    # Returns the estimated position of the robot based on the state probabilities
    # f is the estimate of the state probabilities
    f_position = f.copy()
    for state in range(0, sm.get_num_of_states(), 4):
        f_position[state:state+4] = sum(f_position[state:state+4]) # sum the probabilities of the states in the same position
    return sm.state_to_position(np.argmax(f_position))

if __name__ == '__main__':
    # Task 3) Implementation and 4) Evaluation (uncomment the respective grid size below)
    # grid = (8,8) # 4.1
    # grid = (4,4) # 4.2
    # grid = (16,20) # 4.3
    grid = (10,10) # 4.4
    steps = 100 # number of steps to simulate
    k = 5 # smoother fixed lag
    loops = 10 # number of runs to average over

    # Create the state, transition and observation (sensor) models for the grid
    sm = StateModel(*grid)
    tm = TransitionModel(sm)
    om_UF = ObservationModel_UF.ObservationModelUF(sm)
    om_NUF = ObservationModel_NUF.ObservationModel(sm)

    # vector to store results for averaging over loops
    D_OBS_NUF = np.zeros(steps,dtype='f')
    D_OBS_UF = np.zeros(steps,dtype='f')
    D_EST_NUF = np.zeros(steps,dtype='f')
    D_EST_UF = np.zeros(steps,dtype='f')
    LOOPS_NUF = np.zeros(steps,dtype='i')
    LOOPS_UF = np.zeros(steps,dtype='i')
    D_SMOOTH_NUF = np.zeros(steps-k,dtype='f')

    fail_NUF, fail_UF = 0, 0 # count the number of times the sensor reading fails
    for j in range(loops):
        # Create the HMMFilter(s)
        probs = np.ones(sm.get_num_of_states()) / sm.get_num_of_states() # initial probability distribution
        filter_NUF = HMMFilter(probs, tm, om_NUF, sm)
        filter_UF = HMMFilter(probs, tm, om_UF, sm)
        smoother_NUF = HMMSmoother(tm, om_NUF, sm)
        sensor_r_seq_NUF = np.zeros(k,dtype='i') # sensor readings for smoothing
        f_seq_NUF = np.zeros((k,sm.get_num_of_states()),dtype='f') # filter results for smoothing
        row_k = np.zeros(k,dtype='i') # store the row of the robot k steps ago
        col_k = np.zeros(k,dtype='i') # store the column of the robot k steps ago
        # Create the Robot
        state0 = random.randint(0,sm.get_num_of_states()-1) # random initial pose
        robot = RobotSim(state0,sm)

        # print(f'{"i":>4} {"state":4} {"row,col":4} {"head":4} NUF: {"read":4} {"row,col":4} {"d":>4} {"read":4}  UF: {"row,col":4} {"d":>4}')
        for i in range(steps):
            # simulate robot movement
            state = robot.move_once(tm)
            (row,col,heading) = sm.state_to_pose(state)

            # sensor readings
            reading_NUF = robot.sense_in_current_state(om_NUF)
            if reading_NUF is None:
                fail_NUF += 1
            reading_UF = robot.sense_in_current_state(om_UF)
            if reading_UF is None:
                fail_UF += 1

            if not reading_NUF is None:
                (row_obs_NUF,col_obs_NUF) = sm.reading_to_position(reading_NUF)
                d_obs_NUF= manhattan_distance((row,col),(row_obs_NUF,col_obs_NUF))
                LOOPS_NUF[i] += 1
            else: # skip if no observation
                d_obs_NUF = 0

            if not reading_UF is None:
                (row_obs_UF,col_obs_UF) = sm.reading_to_position(reading_UF)
                d_obs_UF = manhattan_distance((row,col),(row_obs_UF,col_obs_UF))
                LOOPS_UF[i] += 1
            else: # skip if no observation
                d_obs_UF = 0


            # filter update
            est_NUF = filter_NUF.filter(reading_NUF)
            (row_est_NUF,col_est_NUF) = estimate_position(est_NUF, sm)
            d_est_NUF = manhattan_distance((row,col),(row_est_NUF,col_est_NUF))

            est_UF = filter_UF.filter(reading_UF)
            (row_est_UF,col_est_UF) = estimate_position(est_UF, sm)
            d_est_UF = manhattan_distance((row,col),(row_est_UF,col_est_UF))

            # smoother update
            sensor_r_seq_NUF = np.roll(sensor_r_seq_NUF,1) # shift the array to store the previous sensor readings
            sensor_r_seq_NUF[0] = reading_NUF if not reading_NUF is None else om_NUF.get_nr_of_readings()-1
            if i >= k:
                est_smooth_NUF = smoother_NUF.smooth(sensor_r_seq_NUF, f_seq_NUF[-1])
                (row_smooth_NUF,col_smooth_NUF) = estimate_position(est_smooth_NUF, sm)
                d_smooth_NUF = manhattan_distance((row_k[-1],col_k[-1]),(row_smooth_NUF,col_smooth_NUF))
                D_SMOOTH_NUF[i-k] += d_smooth_NUF
            f_seq_NUF = np.roll(f_seq_NUF,1,axis=0) # shift the array to store the previous filter results
            f_seq_NUF[0] = est_NUF
    
            # store results
            D_OBS_NUF[i] += d_obs_NUF
            D_OBS_UF[i] += d_obs_UF
            D_EST_NUF[i] += d_est_NUF
            D_EST_UF[i] += d_est_UF

            row_k = np.roll(row_k,1) # shift the array to store the previous robot position
            col_k = np.roll(col_k,1) # shift the array to store the previous robot position
            row_k[0] = row
            col_k[0] = col

            # print(f'{i:4} {state:4} {row:4},{col:<4} {HEADINGS[heading]:4}     {str(reading_NUF):<4} {row_est_NUF:4},{col_est_NUF:<4} {d_est_NUF:4}     {str(reading_UF):<4} {row_est_UF:4},{col_est_UF:<4} {d_est_UF:4}')
        print(f'Run {j+1}/{loops} completed', end='\r')
    print()

    # compute averages
    fail_NUF /= loops
    fail_UF /= loops
    D_EST_NUF /= loops
    D_EST_UF /= loops
    D_OBS_NUF /= LOOPS_NUF
    D_OBS_UF /= LOOPS_UF
    D_SMOOTH_NUF /= (loops-k)

    print(f'NUF fail frequency {fail_NUF/steps:.2%}, UF fail frequency {fail_UF/steps:.2%}')

    # plot results
    plt.figure()
    plt.plot(D_OBS_NUF, label=f'NUF observations (fail {fail_NUF/steps:.1%})', marker='*')
    plt.plot(D_OBS_UF, label=f'UF observations (fail {fail_UF/steps:.1%})', marker='o')
    plt.plot(D_EST_NUF, label='NUF filter', marker='+')
    plt.plot(D_EST_UF, label='UF filter', marker='x')
    plt.plot(D_SMOOTH_NUF, label='NUF smoother', marker='v')
    plt.xlabel('Step')
    plt.ylabel('Average Manhattan Distance')
    plt.title(f'Forward HMM filter robot localization \nperformance on {grid} grid over {loops} runs')
    plt.legend()
    plt.show()
