#!/usr/bin/env python

################################################################################
# chaser class
#
# Copyright Wind River 2018
#
# 18-01-01 - rhe - written to support relay boards
# 18-02-08 - rhe - Added Trigger and Thread support and timeWarp
# 18-02-18 - tkf - updated to use the latest msgLog class for logging
# 18-02-27 - rhe - Moved sence support and some configuration. Added shim
# shutdown & logging
#
################################################################################
import time
import tty, sys
import RPi.GPIO as GPIO
from subprocess import call
from time import sleep
from collections import deque
import threading

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

import signal

import os

import sys
sys.path.append('../barOak')
sys.path.append('../barOak/home/pi/rellis/barOak')

#from log import log
from msglog import msglog
#from msglog import msglogMail

    


################################################################################
# Class chaserClassconstructor
# Example: myChase = chaser.chaserClass()
################################################################################
#class ioak(log):
#class ioak(msglog, msglogMail):
class ioak(msglog):
    ############################################################################
    # Class constructor
    # Example: myChase = chaser.chaserClass(device)
    #    device:
    #        debug   - print messages only
    #        relay4  - OUT: Relays 0-3 supported
    #                   IN: 
    #        relay8  - OUT: Relays 0-7 supported
    #                   IN: 
    #        Relay16 - OUT: Relays 0-15 supported
    #                   IN:
    ############################################################################
    def __init__ (self, hardwareDevice, filename="log/ioak.log", address=""):

        self.debug = False

        # Constants (tuples)
        self.ioMask = 0x01000
        self.begPat = 0x02000
        self.regPat = 0x00000
        self.revPat = 0x04000
        self.endPat = 0x08000
        self.random_pat = -0x5000
        self.randomTime = -0x5000



        self.color = {
             "off":    (  0,   0,   0),
             "red":    (255,   0,   0),
             "green":  (  0, 255,   0),
             "yellow": (255, 255,   0),
             "blue":   (  0,   0, 255)
            }

        self.tiggerPin=12
        self.shutdownPin=7
                             
        # GPIO BCM number, pin number, mask, TBD (dictionary of tuple elements)
        #             0: ( 3,  5, 0x0001,  1),

        self.ioMgr = {
        #      GPIO,pin,   mask, TBD 
             0: (27, 13, 0x0001,  1),
             1: (22, 15, 0x0002,  2),
             2: ( 5, 29, 0x0004,  3),
             3: ( 6, 31, 0x0008,  4),
             4: (19, 35, 0x0010,  5),
             5: (26, 37, 0x0020,  6),
             6: (20, 38, 0x0040,  7),
             7: (16, 36, 0x0080,  8),
             8: (12, 32, 0x0100,  9),
             9: ( 7, 26, 0x0200, 10),
            10: (18, 12, 0x0400, 11),
            11: (15, 10, 0x0800, 12),
            12: (14,  8, 0x1000, 13),
            13: (17, 11, 0x2000, 14),
            14: (13, 33, 0x4000, 15),
            15: (21, 40, 0x8000, 16)
            }

        #                vlaid ioBed opEnd  board  debug   pMask    piPrj   invrt     
        ioBoardCfg = {
             "debug"   : (True,    0,    8, False,  True,   0xff,  "relay", False),
             "coup4"   : (True,    0,    4,  True, False,   0x0f,  "coup",  False),
             "coup8"   : (True,    0,    8,  True, False,   0xff,  "coup",  False),
             "relay4"  : (True,    0,    4,  True, False,   0x0f,  "relay", False),
             "relay8"  : (True,    0,    8,  True, False,   0xff,  "relay", False),
             "relay8i" : (True,    0,    8,  True, False,   0xff,  "relay", True ),
             "relay16" : (True,    0,   16,  True, False, 0xffff,  "relay", False), 
             "aHat"    : (False,   0,    3, False, False,    0x3,  "relay", False),
             ""        : (False,   0,    0, False, False,    0x0,  "relay", False)
            }
        cfg = ioBoardCfg[hardwareDevice]

        if self.sense == False:
            useSence=False
        else:
            useSence=True
        #log.__init__(self, True, useSence, filename, address)
        msglog.__init__(self, True, useSence, filename, address)
        #msglogMail.__init__(self, True, useSence, filename, address)


        if repr(cfg[0]) == False:
            ioakD.logMsg("WARNING: Unsupported device " + repr(hardwareDevice) + " - Ignoring HW setup")
            self.hwId = "ERROR"
        else:
            self.hwId = hardwareDevice

        self.ioBeg = cfg[1]    
        self.ioEnd = cfg[2]    
        self.board = cfg[3]
        self.debug = cfg[4]
        self.oMask = cfg[5]
        self.piPrj = cfg[6]
        self.invrt = cfg[7]
        self.gpioInit()
 


        # Thread related
        self.shutdownButtonPressed = 0
        self.patThread = False
        self.patThreadAbort = False
        
        # Keyboard
        #tty.setraw(sys.stdin.fileno())       
        return



    
    ############################################################################
    # Method: gpioInit() - Initialize GPIO
    #
    # Initialize GPIO and GPIO out pin
    ############################################################################
    def gpioInit (self):
        # Initialize GPIO pins as output
        #   - GPIO.BOARD - uses the numbering convention on the board
        
        GPIO.setmode(GPIO.BOARD) 
        if self.debug == True:
            GPIO.setwarnings(False)
        else:
            GPIO.setwarnings(False)

        #initialize output GPIO pins
        #GPIO.setup (33, GPIO.OUT) # GPIO13 PWM LED Strip
        #GPIO.setup (12, GPIO.OUT) # GPIO18 PWM LED Strip
        
        # Initialize shutdown call back event
        GPIO.setup (self.shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Shutdown Signal
        GPIO.add_event_detect(self.shutdownPin, GPIO.FALLING, callback=self.shutdownCB, bouncetime=100)
       
        # Initialize input GPIO pins described by the ioMgr[] dictionary
        for ref in range (self.ioBeg, self.ioEnd):
            myGPIO = self.ioMgr[ref]
            pin = myGPIO[1]
            if self.debug == True:
                print ("  DBG: init GPIO " + repr(pin))

            GPIO.setup (pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH) # 1 or any no zero value relay Off





   if False
        
        
        def threadMessage(self, message):
            task = threading.Thread (name = "One More Chance",
                                 target = self.sense.show_message,
                                 args = (message,))
            task.start()



        ############################################################################
        # Method: oneMoreChance() - function to allow user to reboote
        #
        # Called by shutdownCB
        #
        ############################################################################
        def oneMoreChance (self, waitTime):
            print("******** oneMoreChance ********")

            sleep (waitTime)
            if (self.shutdownButtonPressed > 1):
                self.logMsg ("*** System is rebooting")
                self.shutdownCleanup()
                call ("sudo shutdown -r now", shell=True)
            else:
                self.logMsg ("*** System is shutting down")
                self.shutdownCleanup()
                call ("sudo shutdown now", shell=True)


        ############################################################################
        # Method: shutdownCB() - Shutdown callback routine
        #
        # This routine is called whne the GPIO 23 (pin 16) detects a falling edge
        #    - when the shutdown switch is grounded
        ############################################################################
        def shutdownCB (self, extra):
    
            waitTime = 10        # wait for 10 seconds for reboot option

            self.shutdownButtonPressed += 1

            print("******** shutdownCB ********")
            if (self.shutdownButtonPressed == 1):
                self.logMsg1 (1, "*************************************************")
                self.logMsg1 (1, "*** Shutdown button pressed on channel" + repr(extra))
                self.logMsg1 (1, "*** System will power off. ")
                self.logMsg1 (1, "***")
                self.logMsg1 (1, "*** Press shutdown button again to reboot system")
                self.logMsg1 (1, "*************************************************")
                task = threading.Thread (name = "One More Chance",
                                         target = self.oneMoreChance,
                                         args = (waitTime,))
                task.start()
            return


    ############################################################################
    # Method: pattern() - Execute data diven pattern
    #
    # Given a pattern described by myChasePattern, call patternDriver to execute
    # the requested pattern myMaxCount times. 
    # Example: <class>.pattern(10, chasePattern1)
    ############################################################################
    def pattern (self, myMaxCount, myChasePattern):
        self.patternDriver (myMaxCount, myChasePattern, False)
        return


    ############################################################################
    # Method: patternEndState() - Execute data diven pattern
    #
    # Given a pattern described by myChasePattern, call patternDriver to execute
    # the requested pattern myMaxCount times. On completion set circuits to
    # endState.
    # Example: <class>.patternEndState(10, chasePattern1, 0x00)
    ############################################################################
    def patternEndState(self, myMaxCount, myChasePattern, endState):
   
        self.pattern(myMaxCount, myChasePattern, False)
        self.relayPatternSet(self.oMask, endState)
        return 


    ############################################################################
    # Method: patternThread() - Execute data diven pattern in its own thread
    #
    # Given a pattern described by myChasePattern, call patternDriver to execute
    # the requested pattern myMaxCount times within it's own thread. 
    # Example: <class>.patternThread(10, chasePattern1)
    ############################################################################
    def patternThread (self, myMaxCount, myChasePattern):
        if self.patThread != False:
            while self.patThread.isAlive() == True:
                time.sleep(.1)
            
        self.patThread = threading.Thread (name = "Pattern Thread",
                                     target = self.patternDriver,
                                     args = (myMaxCount, myChasePattern, False))
        self.patThreadAbort = False
        self.patThread.start()

        time.sleep(.1) # make sure threads are running before returning
        #return self.patThread.get_ident()
        return 1
        
        
    ############################################################################
    # Method: patternThreadAbort() - Abort current pattern thread
    #
    # Abort the current pattern thread
    # Example: <class>.isThreadAlive()
    ############################################################################
    def patternThreadAbort (self):
       self.patThreadAbort = True
       return self.isThreadAlive()
    

    ############################################################################
    # Method: isThreadAlive() - return True is any pattern threads are alive
    #
    # If the pattern thread alive, return True, otherwise return False
    # Example: <class>.isThreadAlive()
    ############################################################################
    def isThreadAlive(self):
        if self.patThread == False:
            return False
        
        if self.patThread.isAlive() == True:
            return True
        self.patThread = False
        return False


    ############################################################################
    # Method: patternTrigger() - Execute data diven pattern while trigger enable is set
    #
    # Given a pattern described by myChasePattern, execute the pattern
    # myMaxCount times while the trigger GPIO pin is low.
    # Example: <class>.trigger(10, chasePattern1)
    ############################################################################
    def patternTrigger (self, myMaxCount, myChasePattern):
        self.patternDriver (myMaxCount, myChasePattern, True)
        return


    ############################################################################
    # Method: patternDriver() - Execute data diven pattern (Internal Method) 
    #
    # Given a pattern described by myChasePattern, execute the pattern
    # myMaxCount times. 
    # Example: self.patternDriver(10, chasePattern1)
    ############################################################################
    def patternDriver (self, myMaxCount, myChasePattern, triggerCheck):

        myKey = 0
        myDir = 1
        myCount = 0
        myMask = self.oMask
        triggerCount = 0

        while myCount < myMaxCount:
            myCmd = myChasePattern[myKey]
        
                   
            #if self.debug == True:
            #    print ("    DBGz: myCount " + repr(myCount) + " myKey " + repr(myKey)+ " " + repr(myCmd[1]))

            if ((myCmd[0] == self.ioMask)):  # reverce the pattern
                myMask = myCmd[1]
            else:
                if (myCmd[0] == self.begPat):      # start a pattern
                    myDir = 1
         
                elif ((myCmd[0] == self.endPat)):  # end the pattern
                    myKey = -1
                    myCount += 1                

                elif ((myCmd[0] == self.revPat)):  # reverce the pattern
                    myKey -= 1
                    myDir = -1
                    myCount += 1                
 
                # Are we waiting for t=a trigger event?
                if triggerCheck == True:
                    # Wait for a trigger event
                    while GPIO.input(self.tiggerPin) == GPIO.HIGH:
                        if (triggerCount & 0x000ffff) == 1:
                            print ("  Waiting for trigger (" +
                                   repr(triggerCount) + ")")
                        triggerCount += 1
                        time.sleep(.25)
                        
                # Check for abort request (thread mode)
                if self.patThreadAbort == True:
                    self.patThreadAbort = False
                    if self.debug == True:
                        print ("patternDriver() aborting ")
                    return False
                
                # Punch the relays
                self.relayPatternSet(myMask, myCmd[1])

            myKey += myDir
            
            delay = myCmd[2] * self.timeWarp
            if delay > .01:
                time.sleep (delay)

        return True
    

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
    




    ############################################################################
    # Method: ioakDebugPrint() - Print debug information
    #
    # Print debug information.
    # Example: <class>.ioakDebugPrint()
    ############################################################################
    def ioakDebugPrint (self, mydebug=True):
        self.debug = mydebug
        if self.debug == True:          
            self.logMsg1(1, "Debug: ioak")
            self.logMsg1(2, "board               " + repr(self.board))
            self.logMsg1(2, "hwId                " + repr(self.hwId))
            self.logMsg1(2, "begPat              " + "Start of pattern" + repr(hex(self.begPat)) )
            self.logMsg1(2, "regPat              " + "Pattern element" + repr(hex(self.regPat)) )
            self.logMsg1(2, "revPat              " + "Change pattern direction" + repr(hex(self.revPat)) )
            self.logMsg1(2, "io range            " + repr(self.ioBeg)+ "-" + repr(self.ioEnd))
            self.logMsg1(2, "timeWarp            " + repr(self.timeWarp))
            self.logMsg1(2, "shutdownTimer       " + repr(self.shutdownTimer))
            self.logMsg1(2, "sense Hat           " + repr(self.sense))

        return self.debug

if True:
    ############################################################################
    # Method: ioakMain() - Used to debug this class
    #
    # Example: Just execut this script as main to invoke this function
    ############################################################################
    def ioakMain():
        ioakD = ioak("relay8", "myLog.txt", "")
        ioakD.logMsg ("ioak")

    
        ioakD.ioakDebugPrint()
        time.sleep(1)

        while(1):
            time.sleep(1)
        
        print ("ioak.py: Bye")
        return

    if __name__ == "__main__":
        ioakMain()
