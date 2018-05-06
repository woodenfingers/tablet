#!/usr/bin/env python

################################################################################
# Raspberry Pi sence support class
#
# Copyright RHE 2018
#
# 18-03-08 - rhe - written 
#
################################################################################


import time
import sys
sys.path.append('../barOak')
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

    


################################################################################
# Class chaserClassconstructor
# Example: myChase = chaser.chaserClass()
################################################################################
class makeSense():
    ############################################################################
    # Class constructor
    # Example: tw = timeWarpOak()
    ############################################################################
#    def __init__ (self, self.pushedRight, pRefresh=self.refresh):
    def __init__ (self, upCB="", downCB="", leftCB="", rightCB="", refreshCB=""):

        self.sense = False
        self.senseDebug = False

        self.posx=3
        self.posy=3
        self.lastPosx=3
        self.lastPosy=3
        self.setPosDefault()
        self.senseHatInit()                  # initialize sense Hat 

        # Setup joystick functionallity
        if self.sense:
            self.upCB = upCB
            self.downCB = downCB
            self.leftCB = leftCB
            self.rightCB = rightCB
            self.refreshCB = refreshCB
            
            self.sense.stick.direction_up = self.pushedUpReq
            self.sense.stick.direction_down = self.pushedDownReq
            self.sense.stick.direction_left = self.pushedLeftReq
            self.sense.stick.direction_right = self.pushedRightReq
            self.sense.stick.direction_any = self.refreshReq

        return



    def __str__(self):
        return "makeSense"


    def setPosDefault(self):
        self.posx=3
        self.posy=3
        self.lastPosx=3
        self.lastPosy=3
        return
    
    
    ############################################################################
    # Method: senseHatInit() - If sense hat exist, initilaize it
    #
    # set self.sense if a hat exists
    ############################################################################
    def senseHatInit (self):
        try:
            hatProduct = open ("/proc/device-tree/hat/product", "r")
            hatType=hatProduct.read()
            if hatType == "Sense HAT\x00":
                self.sense = SenseHat()
                self.sense.clear()
                if self.senseDebug == True:
                    for n in range(0, 4):
                        self.sense.show_letter('/', [0,0,255])
                        time.sleep(.125)
                        self.sense.show_letter('-', [0,255,0])
                        time.sleep(.125)
                        self.sense.show_letter('\\', [255,0,0])
                        time.sleep(.125)
                        self.sense.show_letter('-', [0,255,0])
                        time.sleep(.125)
                        
                self.sense.show_letter('*', [255,255,255])
                time.sleep(.125)
                self.sense.clear()

            hatProduct.close()

        except:
            self.sense = False
            if self.senseDebug == True:
                print("hatInit No /proc/device-tree/hat/product")
                    
        #pause()
        #print("hatCheck() retrun ")
        return 


    def threadMessage(self, message):
        task = threading.Thread (name = "One More Chance",
                             target = self.sense.show_message,
                             args = (message,))
        task.start()


    ############################################################################
    # Method: clamp() - Return a value clamped between 0 and 7
    #
    # Return a value clamped between 0 and 7
    ############################################################################
    def clamp(self, value, min_value=0, max_value=7):
        return min(max_value, max(min_value, value))



    ############################################################################
    # Method: pushedUpReq() - Joystick was pushed up
    #
    # Decrement self.posy and if a call back routine exists, call it.
    ############################################################################
    def pushedUpReq(self, event):
        if event.action != ACTION_RELEASED:
            self.pushedUpReqWork()
            if self.upCB:
                return self.upCB(event)
        return False

    def pushedUpReqWork(self):
        self.posy = self.clamp(self.posy - 1)
        return


    ############################################################################
    # Method: pushedDownReq() - Joystick was pushed down
    #
    # Increment self.posy and if a call back routine exists, call it.
    ############################################################################
    def pushedDownReq(self, event):
        if event.action != ACTION_RELEASED:
            self.pushedDownReqWork()
            if self.downCB:
                return self.downCB(event)
        return False
    
    def pushedDownReqWork(self):
        self.posy = self.clamp(self.posy + 1)
        return
    
    
    ############################################################################
    # Method: pushedLeftReq() - Joystick was pushed left
    #
    # Decrement self.posx and if a call back routine exists, call it.
    ############################################################################
    def pushedLeftReq(self, event):
        if event.action != ACTION_RELEASED:
            self.posx = self.clamp(self.posx - 1)
            if self.leftCB:
                return self.leftCB(event)
        return False


    ############################################################################
    # Method: pushedRightReq() - Joystick was pushed right
    #
    # Increment self.posx and if a call back routine exists, call it.
    ############################################################################
    def pushedRightReq(self, event):
        if event.action != ACTION_RELEASED:
            self.posx = self.clamp(self.posx + 1)
            if self.rightCB:
                return self.rightCB(event)
        return False


    ############################################################################
    # Method: refreshReq() - All event come here
    #
    # If a call back routine exists, call it.
    ############################################################################
    def refreshReq(self, event):
        if self.refreshCB:
            return self.refreshCB(event)
        return False
      
      
    ############################################################################
    # Method: senseNextPattern() - display next pattern
    #
    # Display next pattern --> 
    ############################################################################
    def senseNextPattern(self, color):
        if self.sense:
            self.jobSenseHide([0,0,0])
            self.jobSenseLine(color)
            self.sense.set_pixel (5, 2, color)                
            self.sense.set_pixel (6, 3, color)                
            self.sense.set_pixel (6, 5, color)                
            self.sense.set_pixel (5, 6, color)                


    ############################################################################
    # Method: sensePrevPattern() - display previous pattern
    #
    # Display previous pattern <-- 
    ############################################################################
    def sensePrevPattern(self, color):
        if self.sense:
            self.jobSenseHide([0,0,0])
            self.jobSenseLine(color)
            self.sense.set_pixel (2, 2, color)                
            self.sense.set_pixel (1, 3, color)                
            self.sense.set_pixel (1, 5, color)                
            self.sense.set_pixel (2, 6, color)



if True:
    class makeSenseTest(makeSense):

        def __init__ (self):
            
            makeSense.__init__(self, "", "", "", "", self.refreshAction)

            self.color = {
            #      GPIO,pin,   mask, TBD 
                 0: (255, 255, 255),
                 1: (255,   0,   0),
                 2: (  0, 255,   0),
                 3: (  0,   0, 255),
                 4: (255, 255,   0),
                 5: (255,   0, 255),
                 6: (  0, 255, 255),
                 7: (128, 128, 128),
            }
            self.colorVal=0
        
        def __str__(self):
            return "makeSenseTest"



        def refreshAction(self, event):
            if event.direction == "middle":
                if event.action == "pressed": 
                    self.colorVal = ((self.colorVal + 1) & 0x07)
            rgb = self.color[self.colorVal]
            self.sense.clear()
            self.sense.set_pixel(self.posx, self.posy, rgb[0], rgb[1], rgb[2])
       
        
        
    ############################################################################
    # Method: lightOakMain() - Used to debug this class
    #
    # Example: Just execut this script as main to invoke this function
    ############################################################################
    def senseTest():
        tSense = makeSenseTest() 
        if tSense.sense:
            #tSense.sense.stick.direction_any = breakJoyStick
            print ("makeSense " + repr(tSense.sense))

            print ("Test Joystick")
            time.sleep(5 * 60 * 1000)
        else:
             print ("makeSense not installed")
           
        
        print ("Bye")
        return
    
    def breakJoyStick():
        print("Hello Broken")

        
    if __name__ == "__main__":
        senseTest()





