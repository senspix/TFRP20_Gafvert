from models import *
from Filters import HMMFilter

import numpy as np
import matplotlib.pyplot as plt
import random


def compare(filter1, filter2 = None, grid = (4,4)):
    pass

def manhattan_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

HEADINGS = ['S', 'E', 'N', 'W']
POSE_ROW = 0
POSE_COL = 1
POSE_HEAD = 2

if __name__ == '__main__':
    # Create the StateModel
    grid = (20,20)
    sm = StateModel(*grid)
    tm = TransitionModel(sm)
    om = ObservationModel_UF.ObservationModelUF(sm)

    # Create the HMMFilter
    probs = np.ones(sm.get_num_of_states()) / sm.get_num_of_states() # initial probability distribution
    filter = HMMFilter(probs, tm, om, sm)

    # Create the Robot
    state = random.randint(0,sm.get_num_of_states()-1) # random initial pose
    robot = RobotSim(state,sm)

    n = 50
    # print(f'{i} Robot: state {state} pose {row,col} {HEADINGS[heading]} Sensor: reading {reading} position {row_read,col_read} Filter: estimate {row_est, col_est} manhattan distance {d}')
    print(f'{"i":3} {"state":5} {"row,col"} {"dir"} {"read"} {"rowr,colr"} {"dr":>4} {"rowe,cole"} {"de":>3}')
    for i in range(n):
        # simulate robot movement
        state = robot.move_once(tm)
        (row,col,heading) = sm.state_to_pose(state)
        # sensor reading

        reading = robot.sense_in_current_state(om)
        (row_read,col_read) = (None,None) if reading == None else sm.reading_to_position(reading)
        dr = None if reading == None else manhattan_distance((row,col),(row_read,col_read))

        # filter update
        estimate = filter.filter(reading)
        (row_est,col_est) = sm.state_to_position(np.argmax(estimate))

        de = manhattan_distance((row,col),(row_est,col_est))

        print(f'{i:3} {state:5} {row:3},{col:<3} {HEADINGS[heading]:3} {str(reading):>4} {str(row_read):>4},{str(col_read):<4} {str(dr):4} {row_est:4},{col_est:<4} {de:3}')
