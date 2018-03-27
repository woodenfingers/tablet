#!/usr/bin/env python

################################################################################
# light class
#
# Copyright Wind River 2018
#
# 18-03-08 - rhe - written 
#
################################################################################


import time
import sys
sys.path.append('../barOak')

from subprocess import call


import buttonshim



    


################################################################################
# Class chaserClassconstructor
# Example: myChase = chaser.chaserClass()
################################################################################
class shimSwitch():
    ############################################################################
    # Class constructor
    # Example: tw = timeWarpOak()
    ############################################################################
#    def __init__ (self, self.pushedRight, pRefresh=self.refresh):
    def __init__ (self, upCB="", downCB="", leftCB="", rightCB="", refreshCB=""):

        try:
            buttonshim.set_pixel(0x00, 0x7f, 0x00)
            self.buttonShimFound = True
            self.shutdownTimer = -100
            self.shimShutDownStop()

        except:
            self.buttonShimFound = False
            
            
        return



    def __str__(self):
        return "shimSwitch"

    ############################################################################
    # Method: shimShutdownStart() - start buttonshim initiated shutdown process 
    #
    # The shutdown process will continue for 7 seconds unles the shim shutdown
    # button is released.
    # Shim buttons are in there own thread
    ############################################################################
    def shimShutdownStart(self):
        if self.shutdownTimer > 0:
            return                    # Debounce: A sutdown is in progress
        
        self.shutdownTimer = 7        # Swich must be held down for 7 seconds 
        self.logMsg1(1, "Shutdown process started.")
        
        self.jobPause == True
        while (self.shutdownTimer > 0):
            self.logMsg1(2, repr(self.shutdownTimer))
            self.sense.show_letter(repr(self.shutdownTimer), (0xff, 0x00, 0x00), (0xf, 0xf, 0xf))
            self.shutdownTimer -= 1
            for count in range (0, 4):            
                if self.shutdownTimer < 0:
                    self.sense.clear()
                    self.jobPause == False
                    self.logMsg("Shutdown process aborted.")
                    return
                buttonshim.set_pixel(0xff, 0x00, 0x00)
                time.sleep(.125)
                buttonshim.set_pixel(0x00, 0x00, 0xff)
                time.sleep(.125)

        buttonshim.set_pixel(0x00, 0x00, 0x00)
        self.sense.clear()
        self.sense.show_letter("S", (0xff, 0x00, 0x00), (0xf, 0xf, 0xf))
        self.logMsg1(2, "Shutdown down now.")
        self.shutdownCleanup()
        self.sense.clear()
        call ("sudo shutdown now", shell=True)
        return


    def shutdownCleanup(self):
        #self.logClose()
        #GPIO.cleanup()
        time.sleep (5)
        return
    
        
    ############################################################################
    # Method: shimShutdownStop() - stop the buttonshim shutdown process 
    #
    # The shutdown will be terminated
    ############################################################################
    def shimShutDownStop(self):
        self.shutdownTimer = -100      
        return

        




if True:
        
        
    ############################################################################
    # Method: lightOakMain() - Used to debug this class
    #
    # Example: Just execut this script as main to invoke this function
    ############################################################################
    def shimSwitchTest():
        tShim = shimSwitch() 
        print ("tShim.buttonShimFound " + repr(tShim.buttonShimFound))

        if tShim.buttonShimFound:
            #tSense.sense.stick.direction_any = breakJoyStick
            print ("shimSwitch is installed " )
            print ("shutdownTimer           " + repr(tShim.shutdownTimer))

        else:
             print ("shimSwitch not installed ")
           
        
        print ("Bye")
        return
    

        
    if __name__ == "__main__":
        shimSwitchTest()





