#!/usr/bin/env python

################################################################################
# light class
#
# Copyright RHE 2018
#
# 18-03-08 - rhe - written 
#
################################################################################


#import sys

    


################################################################################
# Class chaserClassconstructor
# Example: myChase = chaser.chaserClass()
################################################################################
class tempo():
    ############################################################################
    # Class constructor
    # Example: tw = spaceWarpOak()
    ############################################################################
    def __init__ (self):

        self.sense=False
        self.tempoDef = 100
        self.tempo = 0
        self.tempoMax = 0
        self.tempoMin = 0
        self.tempoStep = 10
        self.notesPerBeat = 2
        self.notesPeriod = 0
        self.tempoSetDefault()

        return



    def __str__(self):
        return "tempo Class"


    ############################################################################
    # Method: tempoSetDefault() - set timeWarp to 1.0
    #
    # Set self.timeWarp to 1.0
    ############################################################################
    def tempoSetDefault(self):
        self.tempoStep = 10
        self.notesPerBeat = 2
        return self.tempoSet(self.tempoDef,
                             self.tempoDef + 10,
                             max(20, self.tempoDef - 10))


    ############################################################################
    # Method: timeWarpSet() - set timeWarp
    #
    # Set self.timeWarp to value
    ############################################################################
    def tempoSetMid(self, tempoMin, tempoMax):
        diff=int(tempoMax) - int(tempoMin)
        self.tempoStep = int(max((diff)/8, 1))
        tempo = ((int(tempoMin)) + ((diff)/2))
        return self.tempoSet(tempo, tempoMin, tempoMax) 


    ############################################################################
    # Method: timeWarpSet() - set timeWarp
    #
    # Set self.timeWarp to value
    ############################################################################
    def tempoSet(self, tempo, tempoMin, tempoMax):
        self.tempoMin = tempoMin
        self.tempoMax = tempoMax
        return self.tempoSetCheck(tempo)


    ############################################################################
    # Method: tempoSetCheck() - check timeWarp values
    #
    # timeWarp must be greater than .01
    ############################################################################
    def tempoSetCheck(self, tempo):
        if tempo > self.tempoMax:
            tempo = self.tempoMax
        elif tempo < self.tempoMin:
            tempo = self.tempoMin
        self.tempo = tempo

        self.notesPeriod = (60 / (self.tempo * self.notesPerBeat))
        return self.tempo


    ############################################################################
    # Method: tempoInc() - Slow down time by increasing timeWarp
    #
    # If extra = 38, then increase self.timeWarp by .2
    # Otherwise increase self.timeWarp by extra
    # TODO: do we need a may value?
    ############################################################################
    def tempoInc(self):
        return self.tempoSetCheck(self.tempo + self.tempoStep)
        

    ############################################################################
    # Method: tempoIncCB() - Slow down time by increasing timeWarp Callback
    #
    # timewarp speed up call back. event is ignored
    ############################################################################
    def tempoIncCB(self, event=None):
        self.tempoInc()
        #print("tempoIncCB(" + repr(self.tempo) + ")")
        self.speedSlider()
        return self.tempo


    ############################################################################
    # Method: tempoDec() - Speed up time by reducing timeWarp
    #
    # If extra = 40, then reduce self.timeWarp by .2
    # Otherwise reduce self.timeWarp by extra
    # self.timeWarp is never less than zero
    ############################################################################
    def tempoDec(self):
        return self.tempoSetCheck(self.tempo - self.tempoStep)
        

    ############################################################################
    # Method: tempoDecCB() - Speed up time by reducing timeWarp Callback
    #
    # timewarp speed up call back. event is ignored
    ############################################################################
    def tempoDecCB(self, event=None):
        self.tempoDec()
        #print("tempoDecCB(" + repr(self.tempo) + ")")
        self.speedSlider()
        return self.tempo


    # display slider for timewarp
    def speedSlider(self):
        if self.sense:
            for x in range (0, 8):
                self.sense.set_pixel(x, 7, 0, 100, 255)
            self.sense.set_pixel(7-self.posy, 7, 255, 255, 255)
        return

if True:
    ############################################################################
    # Method: lightOakMain() - Used to debug this class
    #
    # Example: Just execut this script as main to invoke this function
    ############################################################################
    def tempoTest():
        bpm = tempo()
        
        tempoTestPrt(bpm, "tempo(110)")
        print ("tempoMin     " + repr(bpm.tempoMin))
        print ("tempoMax     " + repr(bpm.tempoMax))
        print ("tempoStep    " + repr(bpm.tempoStep))
        print ("notesPerBeat " + repr(bpm.notesPerBeat))
        print ("")
        
        bpm.tempoSetMid(84, 90)
        tempoTestPrt(bpm, "tempoSetMid(84, 90)")
        print ("tempoMin     " + repr(bpm.tempoMin))
        print ("tempoMax     " + repr(bpm.tempoMax))
        print ("tempoStep    " + repr(bpm.tempoStep))
        print ("notesPerBeat " + repr(bpm.notesPerBeat))
        print ("")

        bpm.tempoDec()
        tempoTestPrt(bpm, "tempoDec()")
        
        bpm.tempoDecCB()
        tempoTestPrt (bpm, "tempoDecCB()")
        
        bpm.tempoInc()
        tempoTestPrt (bpm, "tempoInc()")
        
        bpm.tempoIncCB()
        tempoTestPrt (bpm, "tempoIncCB()")
        

        print ("Bye")
        return

    def tempoTestPrt(bpm, title):
        print (title)
        print ("  tempo " + repr(bpm.tempo) + " / period " + repr(bpm.notesPeriod))
        
    if __name__ == "__main__":
        tempoTest()





