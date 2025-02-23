
import random
import numpy as np

from models import *


#
# Add your Filtering / Smoothing approach(es) here
#

def normalize(f):
    return f/np.sum(f)

class HMMFilter:
    def __init__(self, probs, tm, om, sm):
        # if d=0 then forward filtering else smoothing with lag d 
        self.__tm = tm
        self.__om = om
        self.__sm = sm
        self.__f = probs # appears to be uniform (where is this set?)
        # print(probs)
      
 
    # sensorR is the sensor reading (index!), self._f is the probability distribution resulting from the filtering                  
    def filter(self, reading) :
        O = self.__om.get_o_reading(reading) # if failure (None)?
        T = self.__tm.get_T()
        # Updates self.__f per forward filter (AIMA: forward 14.12)
        self.__f = normalize(O@self.__tm.get_T().T@self.__f)
        return self.__f

class HMMSmoother:
    # https://en.wikipedia.org/wiki/Forward%E2%80%93backward_algorithm

    def __init__(self, tm, om, sm):
        self.__tm = tm
        self.__om = om
        self.__sm = sm

    # sensor_r_seq is the sequence (array) with the t-k sensor readings for smoothing, 
    # f_k is the filtered result (f_vector) for step k
    # fb is the smoothed result (fb_vector)
    def smooth(self, sensor_r_seq : np.array, f_k : np.array) -> np.array:
        # fb = self.__f # setting a dummy value here...
        # somehow compute fb to be better than f ;-)
        # ...
        T = self.__tm.get_T()
        b = np.ones(self.__sm.get_num_of_states())
        for i in range(len(sensor_r_seq)):
            O = self.__om.get_o_reading(sensor_r_seq[i])
            b = T@O@b
        fb = normalize(f_k*b)
        return fb