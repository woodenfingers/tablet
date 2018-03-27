#!/usr/bin/env python

################################################################################
# Shutdown Man
#
# Copyright RHE 2018
#
# 18-04-07 - rhe - written 
#
################################################################################


import time
import sys


try:
    import buttonshim
except:
    if False:
        print("Note: buttonshim HW not installed.")

from shutdownMgr import shutdownMgr

shutup = shutdownMgr() 

################################################################################
# Main Do something
################################################################################
def main():

    print (shutup)

    while True:
        time.sleep(10000)
        
    # Program should never return
    print ("ERROR: shutdown Monitor Stopping")
    return True



try:

    @buttonshim.on_press(buttonshim.BUTTON_E)     # Push will start the shutdown process
    def button_e(button, pressed):
        shutup.shimShutdownStart()

    @buttonshim.on_release(buttonshim.BUTTON_E)   # Push will abort the shutdown process
    def button_e(button, release):
        shutup.shutDownStop()
        time.sleep(.125)
        shutup.shutDownStop()
        buttonshim.set_pixel(0x00, 0x00, 0x00)

except:
    if True:
        print("No button shim found")
       


if __name__ == "__main__":
    main()


    



    


