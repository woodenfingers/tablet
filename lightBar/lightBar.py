#!/usr/bin/env python

################################################################################
# lightBar driver
#
# Copyright RHE 2018
#
# 18-04-09 - rhe - written 
#
################################################################################

import time
import sys
sys.path.append('../barOak')

from boxConfig import boxConfig
from dancePatterns import dancePat
from patternLib import patternLib

try:
    import buttonshim
except:
    if False:
        print("Note: buttonshim HW not installed.")




################################################################################
# Main Do something
################################################################################
def main():

    box=boxConfig()
    val = dancePat()
    pat = patternLib()

    myPatternSet = [pat.controlOne,
                    pat.pattern00, pat.pattern01, pat.pattern02, pat.pattern03,
                    pat.pattern04, pat.pattern05, pat.pattern06, pat.pattern07,
                    pat.pattern08,
                    pat.chasePattern11, pat.chasePattern12, pat.chasePattern13,
                    pat.chasePattern20]

    myDanceSet = [pat.pattern00,
                  val.foxTrot, val.waltz,   val.vWaltz, val.tango,
                  val.rumba,   val.rumbaVal]

    myPatAllSet = [pat.controlForever,
                   pat.pattern00, pat.pattern01, pat.pattern02, pat.pattern03,
                   pat.pattern04, pat.pattern05, pat.pattern06, pat.pattern07,
                   pat.pattern08,
                   pat.chasePattern11, pat.chasePattern12, pat.chasePattern13,
                   pat.chasePattern20,
                   val.foxTrot, val.waltz,   val.vWaltz, val.tango,
                   val.rumba,   val.rumbaVal]

    # FIXME: patSet = [pat.controlForever, myPatternSet, myDanceSet]

    box.jobStart(myPatternSet)
        
    print ("Bye.")
    return True


try:
    @buttonshim.on_press(buttonshim.BUTTON_A)     # timewarp Speed up
    def button_a(button, pressed):
        buttonshim.set_pixel(0x94, 0x00, 0xd3)
        val.pushedUpReqWork() 
        val.tempoIncCB()

    @buttonshim.on_press(buttonshim.BUTTON_B)     # timewarp slow down
    def button_b(button, pressed):
        val.posx = val.clamp(val.posx - 1)
        buttonshim.set_pixel(0x00, 0x00, 0xff)
        val.pushedDownReqWork() 
        val.tempoDecCB()


    @buttonshim.on_press(buttonshim.BUTTON_C)     # FIXME: next pattern
    def button_c(button, pressed):
        buttonshim.set_pixel(0x00, 0xff, 0x00)
        val.pushNextActionCB()


    @buttonshim.on_press(buttonshim.BUTTON_D)     # FIXME: prev pattern
    def button_d(button, pressed):
        buttonshim.set_pixel(0xff, 0xff, 0x00)
        val.pushPrevActionCB()


except:
    if True:
        print("No button shim found")
       

if __name__ == "__main__":
    main()


    


