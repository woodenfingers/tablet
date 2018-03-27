#!/usr/bin/env python

################################################################################
# chaser class
#
# Copyright Wind River 2018
#
# 18-03-25 - rhe - written 
# shutdown & logging
#
################################################################################
import time
import tty, sys
#import RPi.GPIO as GPIO
#from subprocess import call
from time import sleep
#from collections import deque
#import threading

   


################################################################################
# Class chaserClassconstructor
# Example: myChase = chaser.chaserClass()
################################################################################
#class ioak(log):
#class ioak(msglog, msglogMail):
class patternDriver():
    ############################################################################
    # Class constructor
    # Example: myChase = chaser.chaserClass(device)
    #    device:
    ############################################################################
    def __init__ (self):
        self.debug = False

        # Constants (tuples)
        self.ioMask = 0x01000
        self.revPat = 0x04000
        self.random_pat = -0x5000
        self.randomTime = -0x5000
        self.myTest="abcdefghijklmnopqustuvwxyz"

        self.begPatDef = (0b10101010, 1.75, 0b00000000,  .25)
        self.endPatDef = (0b00000000, 0)

        self.colorLeter =(
                         #(0xf0, 0xf0, 0xf0),
                         (0xff, 0xff, 0x00),
                         (0x70, 0x70, 0x00),
                         (0xff, 0x00, 0xff),
                         (0x70, 0x00, 0x70),
                         (0x00, 0x70, 0x70),
                         (0x00, 0xff, 0xff),
                         (0x70, 0x00, 0x00),
                         (0xff, 0x00, 0x00),
                         (0x00, 0x70, 0x00),
                         (0x00, 0xff, 0x00),
                         (0x00, 0x00, 0x70),
                         (0x00, 0x00, 0xff)
                         )
        return
   
       
        
    
    
    ############################################################################
    # Method: patternPrint() - Print pattern information
    #
    # Print pattern information
    ############################################################################
    def patternPrint(self, dance, loopCount):
        try:
            name=dance["name"]
        except:
            name="None"
        try:
            style=dance["style"]
        except:
            style="None"
        try:
            bar=dance["bar"]
        except:
            bar=1
            
        print ("Name     " + repr(style) + "/" + name) 
        print ("  bpm    " + repr(self.tempoMin) + " " + repr(self.tempo) + " " + repr(self.tempoMax)) 
        print ("  bar    " + repr(dance["bar"]))
        if loopCount > 0:
            print ("  loop   " + repr(loopCount)) 

        return



    ############################################################################
    # Method: patternTempoSet() - Set pattern tempo
    #
    # Sets pattern tempo midaway between min and max
    ############################################################################
    def patternTempoSet(self, dance):
        try:
            bbmMin=dance["bpm"][0]
        except:
            bbmMin=20
        try:
            bbmMax=dance["bpm"][1]
        except:
            bbmMax=1000
        self.tempoSetMid(bbmMin, bbmMax)
        return



    ############################################################################
    # Method: patternNamePrint() - Print pattern quick name with correct color
    #
    # Print pattern quick name with correct color. the quickname is a single
    # character.
    ############################################################################
    def patternNamePrint(self, dance):
        try:
            style=dance["style"]
        except:
            style="none"
            
        try:
            self.jNameColor = dance["color"]
        except:
            if style == "Ballroom":
                self.jNameColor = (0xff, 0xff, 0x00)
            elif style == "Swing":
                self.jNameColor = (0xff, 0x00, 0xff)
            elif style == "Tango":
                self.jNameColor = (0x00, 0xff, 0xff)
            elif style == "Latin":
                self.jNameColor = (0xff, 0x0f, 0x0f)
            else:
                if dance["class"].lower() == "sequence":
                    self.jNameColor = (0x50, 0x50, 0x50)
                elif dance["class"].lower() == "switch":
                    self.jNameColor = (0xff, 0x0f, 0x0f)
                else:
                    self.jNameColor = (0x0f, 0xff, 0x0f)
                
            
        if self.debug:
            try:
                name=dance["name"]
            except:
                name="-"
            self.sense.show_message(name)
        else:
            try:
                qName=dance["qName"]
            except:
                qName=dance["-"]
            self.sense.show_letter(qName, self.jNameColor)
        return


    
    ############################################################################
    # Method: checkJobPause() - Pause pattern while jobPause is True
    #
    # Pause pattern while jobPause is True
    ############################################################################
    def checkJobPause(self, thisJob):
        while (self.jobPause == True) and (thisJob == self.jobElement):
            #print(".")
            time.sleep(.25)



    ############################################################################
    # Method: patternSwitch() - Play pattern back and forth
    #
    # Play pattern back and forth loopCount times
    # Return 0 if completed Otherwise a not zero indicated the patterned was
    # interupted.
    ############################################################################
    def patternSwitch(self, dance, loopCount):
        thisJob = self.jobElement
        self.patternTempoSet(dance)
        self.patternPrint(dance, loopCount)

        if thisJob == self.jobElement:
            self.patternNamePrint(dance)
        else:
            return -1

        self.playPatternBeg(thisJob, dance)

        while thisJob == self.jobElement and loopCount:
            if loopCount > 0:
                loopCount -= 1

            self.playPattern(thisJob, dance["pat"], None)
            self.checkJobPause(thisJob)
                
            self.playPatternBack(thisJob, dance["pat"], None)
            self.checkJobPause(thisJob)

        self.playPatternEnd(thisJob, dance)
        return loopCount




    
    ############################################################################
    # Method: danceThePattern() - Play pattern 
    #
    # Play pattern loopCount times
    # Return 0 if completed Otherwise a not zero indicated the patterned was
    # interupted.
    ############################################################################
    def danceThePattern(self, dance, loopCount):
        thisJob = self.jobElement
        self.patternTempoSet(dance)
        self.patternPrint(dance, loopCount)

        if thisJob == self.jobElement:
            self.patternNamePrint(dance)
        else:
            return -1
            
        try:
            step = dance["step"] 
        except:
            step = None
            
        self.playPatternBeg(thisJob, dance)

        while thisJob == self.jobElement and loopCount:
            if loopCount > 0:
                loopCount -= 1

            self.playPattern(thisJob, dance["pat"], step)

            #self.playPatternWithIntro(thisJob, dance)
            self.checkJobPause(thisJob)

        self.playPatternEnd(thisJob, dance)
        return loopCount


    
    
    ############################################################################
    # Method: playPatternBeg() - Play beginning pattern sequence
    #
    # If a beginning pattern exist, play the beginning pattern sequence.
    ############################################################################
    def playPatternBeg(self, thisJob, dance):
        try:
            self.playPattern(thisJob, dance["beg"], None)
        except:
            self.playPattern(thisJob, self.begPatDef, None)
        return


    ############################################################################
    # Method: playPatternEnd() - Play ending pattern sequence
    #
    # If an ending pattern exist, play the ending pattern sequence.
    ############################################################################
    def playPatternEnd(self, thisJob, dance):
        try:
            self.playPattern(thisJob, dance["end"], None)
        except:
            self.playPattern(thisJob, self.endPatDef, None)
        return


    ############################################################################
    # Method: playPatternEnd() - Play ending pattern sequence
    #
    # If an ending pattern exist, play the ending pattern sequence.
    ############################################################################
    def playPattern(self, thisJob, pat, letter):
        for index in range (0, len(pat), 2):
            self.playPatternLetter(index, letter)
            
            myLbar=pat[index]
            myRest=pat[index + 1]
            self.relayPatternSet(0xff, myLbar)
            rest = myRest * self.notesPeriod * self.notesPerBeat

            if thisJob != self.jobElement or self.jobPause == True:
                return
            if rest:
                time.sleep(rest)
        return
    

    def playPatternBack(self, thisJob, pat, letter):
        for index in range (len(pat) -1, 0, -2):
            self.playPatternLetter(index, letter)

            myLbar=pat[index - 1]
            myRest=pat[index]
            self.relayPatternSet(0xff, myLbar)
            rest = myRest * self.notesPeriod * self.notesPerBeat

            if thisJob != self.jobElement or self.jobPause == True:
                return
            
            time.sleep(rest)
        return


    def playPatternLetter (self, index, letter):
        if letter:
            index=int(index/2)
            color=self.colorLeter[index & 0x0f]
            self.sense.show_letter(letter[index], color)
        return




    ############################################################################
    # Method: allOn() - Turn on all Relays
    #
    # Call relayPatternSet() to turn on all relays
    ############################################################################
    def allOn (self):
        self.relayPatternSet(0xff, 0b11111111)
        return


    ############################################################################
    # Method: allOff() - Turn off all Relays
    #
    # Call relayPatternSet() to turn off all relays
    ############################################################################
    def allOff (self):
        self.relayPatternSet(0xff, 0b00000000)
        return 


    ############################################################################
    # Method: relayPatternSet() - Automation Hat H/W interface
    #
    # Place pattern element on GPIO pins.
    # Example: myChase.relayPatternSet(pattern)
    ############################################################################
    def relayPatternSet (self, myMask, pattern):
        if False:
            if self.debug == True:
                print ("      DBG: relayPatternSet: " + repr(pattern) + " mask " + repr(myMask))
            
        # Walk pattern and turn on or off each relay
        for ref in range (self.ioBeg, self.ioEnd):
            myGPIO = self.ioMgr[ref]
            if self.invrt == False:
                if myGPIO[2] & myMask:
                    GPIO.output(myGPIO[1], (GPIO.LOW if (pattern & myGPIO[2]) else GPIO.HIGH))
            else:
                if myGPIO[2] & myMask:
                    GPIO.output(myGPIO[1], (GPIO.HIGH if (pattern & myGPIO[2]) else GPIO.LOW))
            if self.sense:
                if myGPIO[2] & myMask:
                    self.sense.set_pixel(ref, 0, (self.color["red"] if (pattern & myGPIO[2]) else self.color["blue"]))

                
        return pattern
    





if True:
    ############################################################################
    # Method: ioakMain() - Used to debug this class
    #
    # Example: Just execut this script as main to invoke this function
    ############################################################################
    def patternMain():
        pat = patternDriver()

    
        #pat.patternDebugPrint()
        time.sleep(1)

        while(1):
            time.sleep(1)
        
        print ("pattern.py: Bye")
        return

    if __name__ == "__main__":
        patternMain()
