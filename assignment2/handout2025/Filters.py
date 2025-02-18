
import random
import numpy as np

from models import *


#
# Add your Filtering / Smoothing approach(es) here
#
class HMMFilter:
    def __init__(self, probs, tm, om, sm, d=0):
        # if d=0 then forward filtering else smoothing with lag d 
        self.__tm = tm
        self.__om = om
        self.__sm = sm
        self.__f = probs # appears to be uniform (where is this set?)
        # print(probs)
        self.__t = 0 # initial time step
        self.__d = d
        self.__B = np.identity(self.__f.shape[0]) if d > 0 else None
        self.__E = np.zeros(1,d) if d > 0 else None
     
    def __forward_filtering(self, O):
        # Updates self.__f per forward filter (AIMA: forward 14.12)
        self.__f = O@self.__tm.get_T().T@self.__f
        alpha = 1/np.sum(self.__f)
        self.__f = self.__f*alpha 
               
    def filter(self, reading) :
        self.__t += 1 # time step
        O = self.__om.get_o_reading(reading) # if failure (None)?
        T = self.__tm.get_T()
        if self.__d == 0:  # forward filtering
            # (AIMA: forward 14.12)
            self.__forward_filtering(O)
        else: # smoothing with lag d
            # (AIMA: Algorithm of Figure 14.6)
            # add sensorR to end of E
            if self.__t > self.__d:
                self.__forward_filtering(O)
                #self.__E.pop(0)

            pass

        # print(np.sum(self.__f))
        return self.__f

        
        
        
