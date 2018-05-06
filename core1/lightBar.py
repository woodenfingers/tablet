#!/usr/bin/python3

################################################################################
# lightBar class
#
# Copyright RHE 2018
#
# 18-05-09 - rhe - ported from someplace 
#
################################################################################
import time
import tty, sys
import RPi.GPIO as GPIO
#import _thread
import threading

from sense_hat import SenseHat

from time import sleep
from tempo import tempo
from hwMgr import hwMgrDef


exitFlag = 0



################################################################################
# Class lightBar
################################################################################
class lightBar(tempo, hwMgrDef):
    ############################################################################
    # Class constructor
    ############################################################################
    def __init__ (self, dictionary=None, loopCount=1, target='relay8i'):


        hwMgrDef.__init__(self, target)
        tempo.__init__(self)

        self.patDebug = True

        self.dict = dictionary
        self.loopCountDef = loopCount
        self.sense = SenseHat()
        
        #self.endPatDef = (0b00000000, 0)

        self.stepColor =(
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
   
        # contro;
        self.playStatus = False
        self.pauseNow = False
        self.isPause = False
        
        # may be defined in dictionary
        self.pName = None
        self.qName = None
        self.style = None
        self.bar = 1
        self.bbmMin = 20
        self.bbmMax = 1000
        self.pClass = 0
        self.step = None
        self.patternBegin = None
        self.pattern = None
        self.patternEnd = None
        self.patColor = None
        self.mask = self.oMask
        self.loopCount = loopCount
        self.timeWarp = 0
        self.resetDefaults()

    
        

    ############################################################################
    # Method: resetDefaults() - Get default vars from pattern dictionary
    ############################################################################
    def resetDefaults(self):
        if 'name' in self.dict:
            self.pName = self.dict['name']
        else:
            self.pName = 'pat'
        
        if 'qName' in self.dict:
            self.qName = self.dict['qName']
        else:
            self.qName = "-"

        if 'style' in self.dict:
            self.style = self.dict['style']
        else:
            self.style = 'None' 

        if 'bar' in self.dict:
            self.bar = self.dict['bar']
        else:
            self.bar = 1

        if 'bpm' in self.dict:
            self.bbmMin=self.dict['bpm'][0]
            self.bbmMax=self.dict["bpm"][1]
        else:
            self.bbmMin = 20
            self.bbmMax = 1000        


        if 'class' in self.dict:
            self.pClass = self.dict['class']
        else:
            self.pClass = 'sequence'

        if 'step' in self.dict:
            self.step = self.dict['step'] 
        else:
            self.step = None

        if 'beg' in self.dict:
            self.patternBegin = self.dict['beg'] 
        else:
            self.patternBegin = None 

        if 'pat' in self.dict:
            self.pattern = self.dict['pat'] 
        else:
            self.pattern = None

        if 'end' in self.dict:
            self.patternEnd = self.dict['end'] 
        else:
            self.patternEnd = (0b00000000, 0)

        self.timeWarpDefault()
        self.colorDefault()
        self.maskDefault()
        self.loopCountDefault()
            
        return


    ############################################################################
    # Method: pause() - Pause the light pattern
    # Method: resume() - Resume the light pattern
    ############################################################################
    def pause(self, mask):
        "Pause the light pattern"
        self.pauseNow = True
    def resume(self):
        "Resume the light pattern"
        self.pauseNow = False
        
        
    ############################################################################
    # Method: pauseCheck() - Pause pattern while self.pause is True
    ############################################################################
    def pauseCheck(self):
        """Pause pattern while self.pauseNow is True
              return imediatly if self.playStatus == False """
        while (self.playStatus == False and self.pauseNow == True):
            self.isPause = True
            time.sleep(.25)
        self.isPause = False
        return self.playStatus


    ############################################################################
    # Method: maskSet() - Set mask
    # Method: maskDefault() - Set default mask
    ############################################################################
    def maskSet(self, mask):
        "set mask"
        self.mask = mask
    def maskDefault(self):
        "set default mask"
        if 'mask' in self.dict:
            self.mask = self.dict['mask']
        else:
            self.mask = self.oMask
        return self.mask



    ############################################################################
    # Method: loopCountSet() - Set loopCount
    # Method: loopCountDefault() - Set default loopCount
    ############################################################################
    def loopCountSet(self, loopCount):
        "set number of time to loop through pattern"
        self.loopCount = loopCount
    def loopCountDefault(self):
        "set number of time to loop through pattern to default"
        self.loopCount = self.loopCountDef



    ############################################################################
    # Method: loopCount() - Set loopCount
    # Method: loopCountDefault() - Set default loopCount
    ############################################################################
    def timeWarpSet(self, timeWarp):
        "set timeWarp "
        self.timeWarp = timeWarp
    def timeWarpDefault(self):
        "set timeWarp to zero - default"
        self.timeWarp = 0


    ############################################################################
    # Method: colorSet() - Set color
    # Method: colorDefault() - Set default color
    ############################################################################
    def colorSet(self, color):
        "set mask"
        self.color = color
    def colorDefault(self):
        "set default mask"
        if 'color' in self.dict:
            self.patColor = self.dict['color']
        else:
            if self.pClass == "sequence":
                self.patColor = (0x50, 0x50, 0x50)
            elif self.pClass == "switch":
                self.patColor = (0xff, 0x0f, 0x0f)
            else:
                self.patColor = (0x0f, 0xff, 0x0f)




    


    def stop(self):
        pStatus = self.playStatus
        self.playStatus = False
        return pStatus


    def play(self):
        self.tempoSetMid(self.bbmMin, self.bbmMax)
        #self.patternPrint()
        self.playStatus = True
        #self.pauseCheck()

        self.playPattern(self.patternBegin, None)
        
        loopCount = self.loopCount
        while self.playStatus == True and loopCount > 0:
            loopCount -= 1

            if self.playPattern(self.pattern, self.step) == False:
                break
            
            self.tempoAdjust(self.timeWarp)

        self.playPattern(self.patternEnd,' ')
        self.playStatus = False

        return loopCount


    ############################################################################
    # Method: patternSwitch() - Play pattern back and forth
    #
    # Play pattern back and forth loopCount times
    # Return 0 if completed Otherwise a not zero indicated the patterned was
    # interupted.
    ############################################################################
    def playSwitch(self):
        self.tempoSetMid(self.bbmMin, self.bbmMax)
        #self.patternPrint()
        self.playStatus = True
        #self.pauseCheck()

        self.playPattern(self.patternBegin, None)

        loopCount = self.loopCount
        while self.playStatus == True and loopCount > 0:
            loopCount -= 1

            if self.playPattern(self.pattern, self.step) == False:
                break
                
            if self.playPatternBack(self.pattern, self.step) == False:
                break
            
            self.tempoAdjust(self.timeWarp)

        self.playPattern(self.patternEnd,' ')
        self.playStatus = False
        return loopCount



    
    


    ############################################################################
    # Method: playPattern() - Play pattern sequence one time
    # Returns False if play is stopped
    ############################################################################
    def playPattern(self, pattern, letter):
        if not pattern == None:
            for index in range (0, len(pattern), 2):
                self.playPatternLetter(index, letter)
            
                myLbar=pattern[index]
                myRest=pattern[index + 1]
                self.relayPatternSet(myLbar)
                rest = myRest * self.notesPeriod * self.notesPerBeat

                if self.pauseCheck() == False:
                    return False
            
                if rest:
                    time.sleep(rest)
        return self.playStatus
    

    ############################################################################
    # Method: playPatternBack() - Play pattern sequence one time
    # Returns False if play is stopped
    ############################################################################
    def playPatternBack(self, pattern, letter):
        if not pattern == None:
            for index in range (len(pattern) -1, 0, -2):
                self.playPatternLetter(index, letter)

                myLbar=pattern[index - 1]
                myRest=pattern[index]
                self.relayPatternSet(myLbar)
                rest = myRest * self.notesPeriod * self.notesPerBeat

                if self.pauseCheck() == False:
                    return False

                if rest:
                    time.sleep(rest)
        return self.playStatus


    ############################################################################
    # Method: playPatternLetter() - Play pattern sequence letter on sence Hat
    # Returns False if play is stopped
    ############################################################################
    def playPatternLetter (self, index, letter):
        if letter:
            index=int(index/2)
            color=self.stepColor[index & 0x0f]
            thisLetter = letter[index]
            self.sense.show_letter(thisLetter, color)
        return




    ############################################################################
    # Method: allOn() - Turn on alllLights with mask
    ############################################################################
    def allOn (self):
        "Turn on all lights with mask"
        self.relayPatternSet(0b11111111)
        return


    ############################################################################
    # Method: set() - Set on light pattern with mask
    ############################################################################
    def set (self, pattern):
        "Set on light pattern with mask"
        self.relayPatternSet(pattern)



    ############################################################################
    # Method: allOff() - Turn off all lights with mask
    ############################################################################
    def allOff (self):
        "Turn off all lights with mask"
        self.relayPatternSet(0b00000000)
        return 


    ############################################################################
    # Method: patternPrint() - Print pattern information
    #
    # Print pattern information
    ############################################################################
    def patternPrint(self):
            
        print ("Name     " + str(self.style) + "/" + self.pName) 
        print ("  bpm    " + repr(self.tempoMin) + " " + repr(self.tempo) + " " + repr(self.tempoMax)) 
        print ("  bar    " + repr(self.bar))
        if int(self.loopCount) > 0:
            print ("  loop   " + repr(self.loopCount)) 

        return



    ############################################################################
    # Method: patternNamePrint() - Print pattern quick name with correct color
    ############################################################################
    def patternNamePrint(self):
        "Print pattern quick name with correct color to the senseHat"          
        if self.patDebug:
            self.sense.show_message(self.pName)
        else:
            self.sense.show_letter(self.qName, self.color)
        return



    ############################################################################
    # Method: relayPatternSet() - Automation Hat H/W interface
    #
    # Place pattern element on GPIO pins.
    # Example: myChase.relayPatternSet(pattern)
    ############################################################################
    def relayPatternSet (self, pattern):
       # if self.patDebug == True:
       #     print ("      DBG: relayPatternSet: " + repr(hex(pattern)) + " mask " + repr(hex(self.mask)))
            
        # Walk pattern and turn on or off each relay
        for ref in range (self.ioBeg, self.ioEnd):
            myGPIO = self.ioMgr[ref]
            if self.invrt == False:
                if myGPIO[2] & self.mask:
                    GPIO.output(myGPIO[1], (GPIO.LOW if (pattern & myGPIO[2]) else GPIO.HIGH))
            else:
                if myGPIO[2] & self.mask:
                    GPIO.output(myGPIO[1], (GPIO.HIGH if (pattern & myGPIO[2]) else GPIO.LOW))
            if self.sense:
                if myGPIO[2] & self.mask:
                    self.sense.set_pixel(ref, 0, (self.color["red"] if (pattern & myGPIO[2]) else self.color["blue"]))

                
        return pattern
    



class playThread(lightBar, threading.Thread):
    def __init__ (self, dictionary=None, loopCount=1, target='relay8i'):

        lightBar.__init__(self, dictionary, loopCount, target)

        threading.Thread.__init__(self)
        self.threadID = self.qName 
        self.name = self.pName
        self.q = None
        
    def run(self):
        self.play()


class playSwitchThread(lightBar, threading.Thread):
    def __init__ (self, dictionary=None, loopCount=1, target='relay8i'):

        lightBar.__init__(self, dictionary, loopCount, target)

        threading.Thread.__init__(self)
        self.threadID = self.qName 
        self.name = self.pName
        self.q = None
        
    def run(self):
        self.playSwitch()

