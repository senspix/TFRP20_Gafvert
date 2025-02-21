from models import *
from Filters import HMMFilter

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
    # Task 3) Implementation
    grid = (8,8)
    # grid = (4,4)
    # grid = (16,20)
    steps = 100 # number of steps to simulate

    # Create the state, transition and observation (sensor) models for the grid
    sm = StateModel(*grid)
    tm = TransitionModel(sm)
    om_UF = ObservationModel_UF.ObservationModelUF(sm)
    om_NUF = ObservationModel_NUF.ObservationModel(sm)

    # Create the HMMFilter(s)
    probs = np.ones(sm.get_num_of_states()) / sm.get_num_of_states() # initial probability distribution
    filter_NUF = HMMFilter(probs, tm, om_NUF, sm)
    filter_UF = HMMFilter(probs, tm, om_UF, sm)

    # Create the Robot
    state0 = random.randint(0,sm.get_num_of_states()-1) # random initial pose
    robot = RobotSim(state0,sm)

    D_OBS_NUF = np.zeros(steps,dtype='f')
    D_OBS_UF = np.zeros(steps,dtype='f')
    D_EST_NUF = np.zeros(steps,dtype='f')
    D_EST_UF = np.zeros(steps,dtype='f')
    LOOPS_NUF = np.zeros(steps,dtype='i')
    LOOPS_UF = np.zeros(steps,dtype='i')

    loops = 500
    fail_NUF, fail_UF = 0, 0
    for j in range(loops):

        # print(f'{"i":>4} {"state":4} {"row,col":4} {"head":4} NUF: {"read":4} {"row,col":4} {"d":>4} {"read":4}  UF: {"row,col":4} {"d":>4}')
        for i in range(steps):
            # simulate robot movement
            state = robot.move_once(tm)
            (row,col,heading) = sm.state_to_pose(state)

            # sensor reading
            reading_NUF = robot.sense_in_current_state(om_NUF)
            if reading_NUF is None:
                fail_NUF += 1
            reading_UF = robot.sense_in_current_state(om_UF)
            if reading_UF is None:
                fail_UF += 1

            if not reading_NUF is None:
                (row_NUF,col_NUF) = sm.reading_to_position(reading_NUF)
                d_obs_NUF= manhattan_distance((row,col),(row_NUF,col_NUF))
                LOOPS_NUF[i] += 1
            else:
                d_obs_NUF = 0

            if not reading_UF is None:
                (row_UF,col_UF) = sm.reading_to_position(reading_UF)
                d_obs_UF = manhattan_distance((row,col),(row_UF,col_UF))
                LOOPS_UF[i] += 1
            else:
                d_obs_UF = 0


            # filter update
            est_NUF = filter_NUF.filter(reading_NUF)
            (row_est_NUF,col_est_NUF) = estimate_position(est_NUF, sm)
            d_est_NUF = manhattan_distance((row,col),(row_est_NUF,col_est_NUF))

            est_UF = filter_UF.filter(reading_UF)
            (row_est_UF,col_est_UF) = estimate_position(est_UF, sm)
            d_est_UF = manhattan_distance((row,col),(row_est_UF,col_est_UF))
    
            D_OBS_NUF[i] += d_obs_NUF
            D_OBS_UF[i] += d_obs_UF
            D_EST_NUF[i] += d_est_NUF
            D_EST_UF[i] += d_est_UF

            # print(f'{i:4} {state:4} {row:4},{col:<4} {HEADINGS[heading]:4}     {str(reading_NUF):<4} {row_est_NUF:4},{col_est_NUF:<4} {d_est_NUF:4}     {str(reading_UF):<4} {row_est_UF:4},{col_est_UF:<4} {d_est_UF:4}')
        print(f'Run {j+1}/{loops} completed', end='\r')
    print()
    fail_NUF /= loops
    fail_UF /= loops
    D_EST_NUF /= loops
    D_EST_UF /= loops
    D_OBS_NUF /= LOOPS_NUF
    D_OBS_UF /= LOOPS_UF

    print(f'NUF fail frequency {fail_NUF/steps:.2%}, UF fail frequency {fail_UF/steps:.2%}')

    plt.figure()
    plt.plot(D_OBS_NUF, label=f'NUF observations (fail {fail_NUF/steps:.1%})', marker='*')
    plt.plot(D_OBS_UF, label=f'UF observations (fail {fail_UF/steps:.1%})', marker='v')
    plt.plot(D_EST_NUF, label='NUF filter', marker='o')
    plt.plot(D_EST_UF, label='UF filter', marker='x')
    plt.xlabel('Step')
    plt.ylabel('Average Manhattan Distance')
    plt.title(f'Forward HMM filter robot localization \nperformance on {grid} grid over {loops} runs')
    plt.legend()
    plt.show()
