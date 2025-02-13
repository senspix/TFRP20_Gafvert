
import random
import numpy as np

from models import *


#
# Add your Filtering / Smoothing approach(es) here
#
class HMMFilter:
    def __init__(self, probs, tm, om, sm):
        self.__tm = tm
        self.__om = om
        self.__sm = sm
        self.__f = probs # appears to be uniform (where is this set?)
        # print(probs)
        
        
    def filter(self, sensorR) :
        # (AIMA: forward 14.12)
        O = self.__om.get_o_reading(sensorR)
        T = self.__tm.get_T()
        self.__f = O@T.T@self.__f
        alpha = 1/np.sum(self.__f)
        self.__f = self.__f*alpha
        # print(np.sum(self.__f))
        return self.__f

        
        
        
