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
import datetime
import sys
import RPi.GPIO as GPIO

from subprocess import call

try:
    import buttonshim
except:
    if False:
        print("Note: buttonshim HW not installed.")


try:
    from sense_hat import SenseHat
except:
    if False:
        print("Note: RPi sence hat not installed.")


    


################################################################################
# Class chaserClassconstructor
# Example: myChase = chaser.chaserClass()
################################################################################
class shutdownMgr():
    ############################################################################
    # Class constructor
    # Example: tw = timeWarpOak()
    ############################################################################
#    def __init__ (self, self.pushedRight, pRefresh=self.refresh):
    def __init__ (self):
        self.shutdownPin=7

        # Define GPIO mode
        GPIO.setmode(GPIO.BOARD) 

        # Initialize shutdown call back event
        GPIO.setup (self.shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Shutdown Signal
        GPIO.add_event_detect(self.shutdownPin, GPIO.FALLING, callback=self.shutdownPinLow, bouncetime=100)

        self.shutdownTimer = -100
        self.shutDownStop()

        try:
            buttonshim.set_pixel(0x00, 0x00, 0x00)
            self.buttonShimFound = True
        except:
            self.buttonShimFound = False

        try:
            self.sense = SenseHat()
        except:
            self.sense=False    
            
        return



    def __str__(self):
        return "Shutdown Manager"





 
    ############################################################################
    # Method: shutdownStart() - Announce shutdown process started 
    #
    # Set Shutdown timer for 7 seconds and announce shutdown process started.
    ############################################################################
    def shutdownStart(self):
        if self.shutdownTimer > 0:
            return False              # Debounce: A sutdown is in progress
        
        self.shutdownTimer = 7        # Swich must be held down for 7 seconds 
        print(datetime.datetime.now())
        print("  Shutdown process started.")
        return True


    ############################################################################
    # Method: shutdownBody() - shutdown body - 1 second 
    #
    # Anounce that the shutdown process in on going for 1 second.
    ############################################################################
    def shutdownBody(self):
        print("    " +repr(self.shutdownTimer))
        if self.sense: self.sense.show_letter(repr(self.shutdownTimer), (0xff, 0x00, 0x00), (0xf, 0xf, 0xf))
        self.shutdownTimer -= 1
        for count in range (0, 4):            
            if self.shutdownTimer < 0:
                return self.shutdownAbort()
            if self.buttonShimFound: buttonshim.set_pixel(0xff, 0x00, 0x00)
            time.sleep(.125)
            if self.buttonShimFound: buttonshim.set_pixel(0x00, 0x00, 0xff)
            time.sleep(.125)
        return


    ############################################################################
    # Method: shutdownAbort() - anounce that the shutdown process is aborted 
    #
    # Anounce that the shutdown process is aborted and return False.
    ############################################################################
    def shutdownAbort(self):
        if self.sense: self.sense.clear()
        #self.jobPause == False
        self.shutDownStop()
        print("Shutdown process aborted.")
        return False
    
    
    ############################################################################
    # Method: shutdownAbort() - kick off the shutdown command 
    #
    # kick off the shutdown command.
    ############################################################################
    def shutdownNow(self):
        print("Shutdown down now.")
        if self.buttonShimFound: buttonshim.set_pixel(0x00, 0x00, 0x00)
        if self.sense: self.sense.clear()
        if self.sense: self.sense.show_letter("S", (0xff, 0x00, 0x00), (0xf, 0xf, 0xf))
        self.shutdownCleanup()
        if self.sense: self.sense.clear()
        call ("sudo shutdown now", shell=True)
        # Just incase th call is not executed
        self.shutDownStop()
        return


    ############################################################################
    # Method: shimShutdownStart() - start buttonshim initiated shutdown process 
    #
    # The shutdown process will continue for 7 seconds unles the shim shutdown
    # button is released.
    # Shim buttons are in there own thread
    ############################################################################
    def shutdownCleanup(self):
        # TODO figure out how to stop running processes
        #self.logClose()
        #GPIO.cleanup()
        #time.sleep (5)
        return


    ############################################################################
    # Method: shutdownPinLow() - start pin initiated shutdown process 
    #
    # The shutdown process will continue for 7 seconds unles the shutdown pin
    # is released.
    # pins processed in own thread
    ############################################################################
    def shutdownPinLow(self, extra):
        if self.shutdownStart() == False:
            return False
        
        while self.shutdownTimer > 0:
            if (GPIO.input(self.shutdownPin) == GPIO.LOW):
                self.shutdownBody()
            else:
                # pin was prematurllly raised - abort shutdown
                return self.shutdownAbort()
                
        self.shutdownNow()     
        return
    

    ############################################################################
    # Method: shimShutdownStart() - start buttonshim initiated shutdown process 
    #
    # The shutdown process will continue for 7 seconds unles the shim shutdown
    # button is released.
    # Shim buttons are in there own thread
    ############################################################################
    def shimShutdownStart(self):
        if self.shutdownStart() == False:
            return False
        
        #self.jobPause == True
        while (self.shutdownTimer > 0):
            self.shutdownBody()
            
        # self.shutdownTimer < 0 if process aborted
        if self.shutdownTimer < 0:
            return self.shutdownAbort()
        
        self.shutdownNow()
        return


    
        
    ############################################################################
    # Method: shutDownStop() - stop the buttonshim shutdown process 
    #
    # The shutdown will be terminated
    ############################################################################
    def shutDownStop(self):
        self.shutdownTimer = -100      
        return


def main():
    print("Try running shutdownMan.py")
    #subprocess.call(['gnome-terminal',' -e', ' python /home/pi/git/tablet/tShutdown/shutdownMan.py'])

if __name__ == "__main__":
    main()


        
        