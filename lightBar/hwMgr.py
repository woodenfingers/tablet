#!/usr/bin/env python

################################################################################
# chaser class
#
# Copyright Wind River 2018
#
# 18-04-06 - rhe - ported from dkofun
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
#from msglog import msglog
#from msglog import msglogMail

    


################################################################################
# Class chaserClassconstructor
# Example: myChase = chaser.chaserClass()
################################################################################
#class ioak(log):
#class ioak(msglog, msglogMail):
class hwMgr():
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
    def __init__ (self, hardwareDevice):

        self.debug = False

        self.tiggerPin=12
                             
        self.color = {
            "off":    (  0,   0,   0),
            "red":    (255,   0,   0),
            "green":  (  0, 255,   0),
            "yellow": (255, 255,   0),
            "blue":   (  0,   0, 255)
            }

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
        try:
            cfg = ioBoardCfg[hardwareDevice]
            self.hwId = hardwareDevice
            self.ioBeg = cfg[1]    
            self.ioEnd = cfg[2]    
            self.board = cfg[3]
            self.debug = cfg[4]
            self.oMask = cfg[5]
            self.piPrj = cfg[6]
            self.invrt = cfg[7]
        except:
            print("WARNING: Unsupported device " + repr(hardwareDevice) + " - Ignoring HW setup")
            self.hwId = "ERROR"
            self.ioBeg = 0    
            self.ioEnd = 0    
            self.board = "ERROR"
            self.debug = True
            self.oMask = 0
            self.piPrj = "ERROR"
            self.invrt = False
            print ("self.invrt " + self.invrt)
            return
        

        self.gpioInit()
 

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
        
       
        # Initialize input GPIO pins described by the ioMgr[] dictionary
        for ref in range (self.ioBeg, self.ioEnd):
            myGPIO = self.ioMgr[ref]
            pin = myGPIO[1]
            if self.debug == True:
                print ("  DBG: init GPIO " + repr(pin))

            GPIO.setup (pin, GPIO.OUT)
            if self.invrt:
                GPIO.output(pin, GPIO.LOW) 
            else:
                GPIO.output(pin, GPIO.HIGH) # 1 or any no zero value relay Off



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
            print("Debug: ioak")
            print("board               " + repr(self.board))
            print("hwId                " + repr(self.hwId))
            print("io range            " + repr(self.ioBeg)+ "-" + repr(self.ioEnd))
            print("  board             " + repr(self.board))    
            print("  debug             " + repr(self.debug))    
            print("  oMask             " + repr(self.oMask))    
            print("  piPrj             " + repr(self.piPrj))    
            print("  invrt             " + repr(self.invrt))    

        return self.debug

if True:
    ############################################################################
    # Method: ioakMain() - Used to debug this class
    #
    # Example: Just execut this script as main to invoke this function
    ############################################################################
    def hwMgrMain():
        ioakD = hwMgr("relay8i")
        print ("hwMgrMain")

    
        ioakD.ioakDebugPrint()
        time.sleep(1)

        while(1):
            time.sleep(1)
        
        print ("hwMgrMain.py: Bye")
        return

    if __name__ == "__main__":
        hwMgrMain()
