from models import *
from Filters import HMMFilter

import numpy as np
import matplotlib.pyplot as plt
import random


def manhattan_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


def compare(grid_size, filter1, filter2 = None, n = 500, ):
    pass


HEADINGS = ['S', 'E', 'N', 'W']
POSE_ROW = 0
POSE_COL = 1
POSE_HEAD = 2

def failed():
        # Task 3) Implementation
    grid = (8,8)
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

    state = np.zeros(steps,dtype='i')
    row = np.zeros(steps,dtype='i')
    col = np.zeros(steps,dtype='i')
    heading = np.zeros(steps,dtype='i')
    reading_NUF = np.zeros(steps,dtype='i')
    reading_UF = np.zeros(steps,dtype='i')
    row_NUF = np.zeros(steps,dtype='i')
    col_NUF = np.zeros(steps,dtype='i')
    row_UF = np.zeros(steps,dtype='i')
    col_UF = np.zeros(steps,dtype='i')
    d_NUF = np.zeros(steps,dtype='i')
    d_UF = np.zeros(steps,dtype='i')
    state_est_NUF = np.zeros(steps,dtype='i')
    row_est_NUF = np.zeros(steps,dtype='i')
    col_est_NUF = np.zeros(steps,dtype='i')
    d_est_NUF = np.zeros(steps,dtype='i')
    state_est_UF = np.zeros(steps,dtype='i')
    row_est_UF = np.zeros(steps,dtype='i')
    col_est_UF = np.zeros(steps,dtype='i')
    d_est_UF = np.zeros(steps,dtype='i')
    

    # print(f'{i} Robot: state {state} pose {row,col} {HEADINGS[heading]} Sensor: reading {reading} position {row_read,col_read} Filter: estimate {row_est, col_est} manhattan distance {d}')
    print(f'{"i":3} {"state":5} {"row,col"} {"dir"} {"read"} {"rowr,colr"} {"dr":>4} {"rowe,cole"} {"de":>3}')
    for i in range(steps):
        # simulate robot movement
        state[i] = robot.move_once(tm)
        (row[i],col[i],heading[i]) = sm.state_to_pose(state[i])

        # sensor reading
        reading = robot.sense_in_current_state(om_NUF)
        reading_NUF[i] = reading
        reading = robot.sense_in_current_state(om_UF)
        reading_UF[i] = reading

        (row_NUF[i],col_NUF[i]) = sm.reading_to_position(reading_NUF[i])
        (row_UF[i],col_UF[i]) = sm.reading_to_position(reading_UF[i])

        d_NUF[i] = manhattan_distance((row[i],col[i]),(row_NUF[i],col_NUF[i]))
        d_UF[i] = manhattan_distance((row[i],col[i]),(row_UF[i],col_UF[i]))

        # filter update
        estimate = filter_NUF.filter(None if np.isnan(reading_NUF[i]) else reading_NUF[i])
        state_est_NUF[i] = np.argmax(estimate)
        (row_est_NUF[i],col_est_NUF[i]) = sm.state_to_position(state_est_NUF[i])
        d_est_NUF[i] = manhattan_distance((row[i],col[i]),(row_est_NUF[i],col_est_NUF[i]))

        estimate = filter_UF.filter(None if np.isnan(reading_UF[i]) else reading_UF[i])
        state_est_UF[i] = np.argmax(estimate)
        (row_est_UF[i],col_est_UF[i]) = sm.state_to_position(state_est_UF[i])
        d_est_UF[i] = manhattan_distance((row[i],col[i]),(row_est_UF[i],col_est_UF[i]))

        # print(f'{i:3} {state:5} {row:3},{col:<3} {HEADINGS[heading]:3} {str(reading):>4} {str(row_read):>4},{str(col_read):<4} {str(dr):4} {row_est:4},{col_est:<4} {de:3}')

def estimate_position(f, sm):
    # Returns the estimated position of the robot based on the state probabilities
    # f is the estimate of the state probabilities
    f_position = f.copy()
    for state in range(0, sm.get_num_of_states(), 4):
        f_position[state:state+4] = sum(f_position[state:state+4])
    return sm.state_to_position(np.argmax(f_position))

if __name__ == '__main__':
    # Task 3) Implementation
    grid = (15,15)
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


    # print(f'{i} Robot: state {state} pose {row,col} {HEADINGS[heading]} Sensor: reading {reading} position {row_read,col_read} Filter: estimate {row_est, col_est} manhattan distance {d}')
    # print(f'{"i":3} {"state":5} {"row,col"} {"dir"} {"read"} {"rowr,colr"} {"dr":>4} {"rowe,cole"} {"de":>3}')
    print(f'{"i":>4} {"state":4} {"row,col":4} {"head":4} NUF: {"read":4} {"row,col":4} {"d":>4} {"read":4}  UF: {"row,col":4} {"d":>4}')
    fail_NUF, fail_UF = 0, 0
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

        # Commented out below: reading_to_position does not handle None gracefully
        # (row_NUF,col_NUF) = sm.reading_to_position(reading_NUF)
        # (row_UF,col_UF) = sm.reading_to_position(reading_UF)

        # d_NUF= manhattan_distance((row,col),(row_NUF,col_NUF))
        # d_UF = manhattan_distance((row,col),(row_UF,col_UF))

        # filter update
        est_NUF = filter_NUF.filter(reading_NUF)
        (row_est_NUF,col_est_NUF) = estimate_position(est_NUF, sm)
        d_est_NUF = manhattan_distance((row,col),(row_est_NUF,col_est_NUF))

        est_UF = filter_UF.filter(reading_UF)
        (row_est_UF,col_est_UF) = estimate_position(est_UF, sm)
        d_est_UF = manhattan_distance((row,col),(row_est_UF,col_est_UF))
 

        # print(f'{i:3} {state:5} {row:3},{col:<3} {HEADINGS[heading]:3} {str(reading):>4} {str(row_read):>4},{str(col_read):<4} {str(dr):4} {row_est:4},{col_est:<4} {de:3}')
        print(f'{i:4} {state:4} {row:4},{col:<4} {HEADINGS[heading]:4}     {str(reading_NUF):<4} {row_est_NUF:4},{col_est_NUF:<4} {d_est_NUF:4}     {str(reading_UF):<4} {row_est_UF:4},{col_est_UF:<4} {d_est_UF:4}')
    print(f'NUF fail frequency {fail_NUF/steps:.2%}, UF fail frequency {fail_UF/steps:.2%}')