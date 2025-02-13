
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
        self.__f = probs # where is this set?
        
        
    def filter(self, sensorR) :
        #print( self.__f)
        # (forward 14.12)
        # O = self.__om.get_o_reading(sensorR)
        # T = self.__tm. get_T_transpose()
        # self.__f = 
        # (backward 14.13)
        #...
        return self.__f

        
        
        
