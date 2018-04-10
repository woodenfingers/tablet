#!/usr/bin/env python

################################################################################
# msg class
#
# Copyright RHE 2018
#
# 18-04-09 - rhe - written
#
################################################################################

import datetime
import time

################################################################################
# Class log
################################################################################
class log:

    ############################################################################
    # Class constructor
    # Example: logger = msglog.msglog (toConsole, toSense, filename, address)
    #    - toConsole - boolean value - display message to terminal if True
    #    - toSense - boolean value - display message to sense screen if True
    #    - filename - string - full pathname to file to write message to
    #    - address - string - address of text recipient to send message as text
    ############################################################################
    def __init__ (self, toConsole=True, toSense=False, filename=""):
        print ("log __init__: toConsole " + repr(toConsole) + " toSense " + repr(toSense) + " filename " + repr(filename))

        self.toConsole = toConsole
        self.toSense = toSense

        # file support
        self.toFs = False
        self.fd = False
        self.fdIsOpen = False
        self.filename = filename
        if (self.filename != ''):
            try:
                self.fd = open (self.filename, "a+")
                self.toFs = True
                self.fdIsOpen = True
            except:
                print("WARNING: Unable to open file " + self.filename)
            
        return

    ############################################################################
    # Method: logClose - graceful shutdown 
    #
    # Closed open files
    # Example:
    #     <class>.logClose ("")
    ############################################################################
    def logClose(self):
        if (self.fd == True) & (self.fdIsOpen == True):
            close(self.id)
        self.fdIsOpen = False
        return


    ############################################################################
    # Method: logMsg1 - Log message with indent
    #
    # Log message as with level as folows:
    #   If console enabled, write message with timestame for all levels
    #   If file enabled, write message with timestame for all levels
    #   If text sense hat, write only level 0 messages without a timestamp    
    #   If text enabled, write only level 0 messages without a timestamp    
    # Returns value > 0 on success otherwise 0
    # Example:
    #     <class>.msgLog (0, "My message")
    ############################################################################
    def logMsg1(self, level, message):
        istr = ""
        for x in range (0, level * 2):
            istr = istr + " "

        message = istr + message
        messageTc = repr(time.ctime()) + " : " + message

        written  = self.logToConsole(messageTc)
        written += self.logToFile(messageTc)
        
        # Only send level zero messages to text or sence
        if level == 0:
            written += self.logToSense(message)
        
        return written


    ############################################################################
    # Method: msgLog - Log message 
    #
    # Call logMsg() to Log the message as follows:
    # Example:
    #     <class>.msgLog ("My message")
    ############################################################################
    def logMsg(self, message):
        return self.logMsg1(0, message)
    

    ############################################################################
    # Method: logToConsole - if cosole enabled, write message to console 
    #
    # If console enabled, write message to the console and return 1.
    # Otherwise return 0
    # Example:
    #     <class>.logToConsole ("My message")
    ############################################################################
    def logToConsole(self, message):
        if self.toConsole == True:
            print (message)
            return 1
        else:
            return 0


    ############################################################################
    # Method: logToFile - if file is enabled, write message to file 
    #
    # If file is enabled, write message to the file and return 1.
    # Otherwise return 0
    # Example:
    #     <class>.logToFile ("My message")
    ############################################################################
    def logToFile(self, message):
        if self.toFs == True:
            self.fd.write (message + "\r")
            return 1
        else:
            return 0


    ############################################################################
    # Method: logToSense - if sense hat enabled, write message to sence hat 
    #
    # If sense hat enabled, write message to the sense hat and return 1.
    # Otherwise return 0
    # Example:
    #     <class>.logToSense ("My message")
    ############################################################################
    def logToSense(self, message):
        if self.toSense == True:
            self.sense.show_message(message)
            return 1
        else:
            return 0

     
if True:
    ############################################################################
    # Method: logMain() - Used to debug this class
    #
    # Example: Just execut this script as main to invoke this function
    ############################################################################
    def logMain():
        logD = log(True, False, "./myDebugFile")
        #logD = log(True, False, "/mnt/gdrivefs/test/thisIsABadFileName.txt") 
        print ("logD.fd        " + repr(logD.fd))
        print ("logD.fdIsOpen  " + repr(logD.fdIsOpen))
        print ("logD.toFs      " + repr(logD.toFs))
        print ("logD.toConsole " + repr(logD.toConsole)) 
        print ("logD.toSense   " + repr(logD.toSense))
        print ("logD.toText    " + repr(logD.toText))

        logD.logMsg("log.py: Debugging")
        
        logD.logMsg1(0, "level 0")
        logD.logMsg1(1, "level 1")
        logD.logMsg1(2, "level 2")
        logD.logMsg1(5, "level 5")

        fly=8
        logD.logMsg1(0, "fly:")
        logD.logMsg1(1, "my fly: " + repr(fly))

        logD.logMsg("Bye")

        return

    if __name__ == "__main__":
        logMain()
