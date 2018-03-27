#!/usr/bin/env python

################################################################################
# lightBar driver
#
# Copyright Wind River 2018
#
# 18-02-08 - rhe - written 
#
################################################################################

import time
import sys
sys.path.append('../barOak')

from dancePatterns import dancePat

val = dancePat() 

try:
    import buttonshim
except:
    if False:
        print("Note: buttonshim HW not installed.")



chasePattern00 = {
                "class" : "sequence",
                "name"  : ("Off"),
                "qName" : ("X"),
                "bpm"   : (100, 600), #
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : (0b00000000, 0),
                "pat"   : (0b00000000, 1),              
                "end"   : (0b00000000, 0)
                }

chasePattern01 = {
                "class" : "sequence",
                "name"  : ("Chase 1"),
                "qName" : ("1"),
                "bpm"   : (100, 600), #
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : (0b00000000,  .5),
                "pat"   : (0b00000001,  .5,
                           0b00000010,  .5,
                           0b00000100,  .5,
                           0b00001000,  .5,
                           0b00010000,  .5,
                           0b00100000,  .5,
                           0b01000000,  .5,                
                           0b10000000,  .5),              
                "end"   : (0b00000000, 0)
                }



chasePattern02 = {
                "class" : "sequence",
                "name"  : ("Chase 2"),
                "qName" : ("2"),
                "bpm"   : (100, 600), #
                "bar"   : (4),
                "mask"  : (0xf0),
                "beg"   : (0b00000000, 0),
                "pat"   : (0b00010001, 1,
                           0b00100010, 1,
                           0b01000100, 1,
                           0b10001000, 1,
                           0b00100000, 1,
                           0b01000000, 1,                
                           0b10000000, 1),              
                "end"   : (0b10000000, 0)
                }

chasePattern03 = {
                "class" : "sequence",
                "name"  : ("Chase 3"),
                "qName" : ("3"),
                "bpm"   : (100, 600), #
                "bar"   : (4),
                "mask"  : (0x0f),
                "beg"   : (0b00000000, 0),
                "pat"   : (0b10101010, 1,
                           0b01010101, 1),              
                "end"   : (0b01010101, 0)
                }



chasePattern10 = {
                "class" : "switch",
                "name"  : ("switch back 9"),
                "qName" : ("9"),
                "color" : (0xff, 0x0f, 0xf0),
                "bpm"   : (100,1000), #
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : (0b00000000, 1),
                "pat"   : (0b00000001, 1,
                           0b00000011, 1,
                           0b00000110, 1,
                           0b00001100, 1,
                           0b00011000, 1,
                           0b00110000, 1,                
                           0b11000000, 1,                
                           0b10000000, 1),              
                "end"   : (0b00000000, 0)
                }

controlForever = {
                "class"      : "control",
                "name"       : ("forever"),
                "jobSetCount"  : -1,
                "jobLoopCount" : -1
                }
controlOne = {
                "class"        : "control",
                "name"         : ("forever"),
                "jobSetCount"  : 1,
                "jobLoopCount" : 1
                }


################################################################################
# Main Do something
################################################################################
def main():

    myDanceSet = [controlForever, chasePattern00, chasePattern10,
                  val.foxTrot, val.waltz,   val.vWaltz, val.tango,
                  val.rumba,   val.rumbaVal,
                  chasePattern01, chasePattern02,
                  chasePattern03]

    
    while True:
        val.jobStart(myDanceSet)
        
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


    




import time
import sys
sys.path.append('../barOak')

#import lightOak 
#val = lightOak.lightOak("relay8", "log/lightBarLog.txt", "") 

try:
    import buttonshim
except:
    if False:
        print("Note: buttonshim HW not installed.")





################################################################################
# Main Do something
################################################################################
def main():



    print ("Bye.")
    return True


try:
    @buttonshim.on_press(buttonshim.BUTTON_A)     # timewarp Speed up
    def button_a(button, pressed):
        buttonshim.set_pixel(0x94, 0x00, 0xd3)
        val.pushUpAction()
        #val.refresh()

    @buttonshim.on_press(buttonshim.BUTTON_B)     # timewarp slow down
    def button_b(button, pressed):
        buttonshim.set_pixel(0x00, 0x00, 0xff)
        val.pushDownAction()
        #val.refresh()


    @buttonshim.on_press(buttonshim.BUTTON_C)     # FIXME: next pattern
    def button_c(button, pressed):
        buttonshim.set_pixel(0x00, 0xff, 0x00)
        val.pushRightAction()
        #val.refresh()

    @buttonshim.on_press(buttonshim.BUTTON_D)     # FIXME: prev pattern
    def button_d(button, pressed):
        buttonshim.set_pixel(0xff, 0xff, 0x00)
        val.pushLeftAction()
        #val.refresh()


    @buttonshim.on_press(buttonshim.BUTTON_E)     # Push will start the shutdown process
    def button_e(button, pressed):
        val.shimShutdownStart()

    @buttonshim.on_release(buttonshim.BUTTON_E)   # Push will abort the shutdown process
    def button_e(button, release):
        buttonshim.set_pixel(0x00, 0xff, 0x00)
        val.shimShutDownStop()

except:
    if True:
        print("No button shim found")
       


if __name__ == "__main__":
    main()


    


