#!/usr/bin/env python

################################################################################
# boxConfig class
#
# Copyright RHE 2018
# Define the project
#
# 18-03-08 - rhe - written 
#
################################################################################

import time
import sys
sys.path.append('../barOak')

from hwMgr import hwMgr
from log import log
from hwMakeSense import makeSense
from tempo import tempo
from patternDriver import patternDriver
from jobList import jobList

    


################################################################################
# Class chaserClassconstructor
# Example: myChase = chaser.chaserClass()
################################################################################
class boxConfig(hwMgr, jobList, log, makeSense, tempo, patternDriver):
    ############################################################################
    # Class constructor
    # Example: tw = boxConfig()
    ############################################################################
    #def __init__ (self, logFile="./log/boxConfig.log", twDef=1.0):
    def __init__ (self, logFile=""):

        self.sense = False
        
        hwMgr.__init__(self, "relay8i")

        jobList.__init__(self)

        patternDriver.__init__(self)

        tempo.__init__(self)

        #makeSense.__init__(self, self.timeWarpAddCB, self.timeWarpSubCB, self.pushPrevActionCB, self.pushNextActionCB, self.boxConfigRefreshCB)
        makeSense.__init__(self, self.tempoIncCB, self.tempoDecCB, self.pushPrevActionCB, self.pushNextActionCB, self.boxConfigRefreshCB)


        log.__init__(self, True, self.sense, logFile)
        self.logMsg("boxConfig: Begin")


        #addLightManagerClassHere
        self.lMgr0=0
        self.lMgr1=1
        self.lMgr2=2
        self.lMgr = (self.lMgr0, self.lMgr1, self.lMgr2)

        myLen = len(self.lMgr)
        #for n in range (0, myLen):
        #    print("  self.lMgr " + repr(self.lMgr[n]))
        #addLightManagerClassHere
        

        return



    def __str__(self):
        return "boxConfig"
    
    


    def shimTimeWarpSub(self):
        self.posy = self.clamp(self.posy - 1)
        self.timeWarpSubCB()

    def shimTimeWarpAdd(self):
        self.posy = self.clamp(self.posy + 1)
        self.timeWarpAddCB()


if True:
    
    ############################################################################
    # Method: lightOakMain() - Used to debug this class
    #
    # Example: Just execut this script as main to invoke this function
    ############################################################################
    def boxConfigTest():


        sp = boxConfig() 
        print ("boxConfigTest " + repr(sp.tempo))

        while True:
            time.sleep(1)
        
        print ("Bye")
        return

    if __name__ == "__main__":
        boxConfigTest()



