#!/usr/bin/env python

################################################################################
# boxConfig class
#
# Copyright Wind River 2018
# Define the project
#
# 18-03-08 - rhe - written 
#
################################################################################

import time
import sys
sys.path.append('../barOak')


    


################################################################################
# Class chaserClassconstructor
# Example: myChase = chaser.chaserClass()
################################################################################
class jobList():
    ############################################################################
    # Class constructor
    # Example: tw = boxConfig()
    ############################################################################
    #def __init__ (self, logFile="./log/boxConfig.log", twDef=1.0):
    def __init__ (self):

       
        self.jobDebugFlag = True
        self.jobElement   = 0
        self.jobMax       = 0
        self.jobList      = False
        self.jobTask      = False
        self.jobPause     = False
        self.jobRest      = False  # Pause between Jobs
        self.jobDirection = 1 

        self.jName        = " "    # quick name
        self.jNameColor   = (0x70, 0x70, 0)

        self.jobSetCount  = -1  # Number of jobs to run Forever  
        self.jobLoopCount = -1  # Number of times to run individual job  
        self.jobSetCount = 1  # Number of jobs to run Forever  
        self.jobLoopCount = 1  # Number of times to run individual job  


        return



    def __str__(self):
        return "jobList"

   
    ############################################################################
    # Method: jobSet() - Set a list defined job
    #
    # If self.jobList exist, then set self.jobTask to the lisst defined by
    # self.jobElement
    ############################################################################
    def jobSet(self):
        if self.jobList:
            self.jobTask=self.jobList[self.jobElement]
            try:
               self.jName = self.jobTask["qName"]
            except:
               None

            try:
               self.jNameColor = self.jobTask["color"]
            except:
               None

            try:
               self.jName = self.jobTask["qName"]
            except:
               None

            try:
               self.jobRest = self.jobTask["jobRest"]
            except:
               None

            try:
               self.jobSetCount = int(self.jobTask["jobSetCount"])
            except:
               None

            try:
               self.jobLoopCount = int(self.jobTask["jobLoopCount"])
            except:
               None

            if self.jobDebugFlag == True:
                self.jobDebug()
                
            if self.jobPause == False:
                self.jobPause = self.jobRest
            print("jobSet() jobTask[class]" + self.jobTask["class"])
        return


    ############################################################################
    # Method: jobStart() - Start a list of jobs
    #
    # If self.jobList exist, then set self.jobTask to the lisst defined by
    # self.jobElement
    ############################################################################
    def jobStart(self, jobList):
        complete = 0

        self.jobList=jobList
        self.jobElement=0
        self.jobMax = len(self.jobList)
        self.jobSet()
        jobLoop = self.jobSetCount
        
        while jobLoop != 0:
                
            self.setPosDefault()
            self.allOff()
            pattern = self.jobList[self.jobElement]
            
            if pattern["class"].lower() == "dance":
                complete = self.danceThePattern(pattern, self.jobLoopCount) 
            elif pattern["class"].lower() == "sequence":
                complete = self.danceThePattern(pattern, self.jobLoopCount)
            elif pattern["class"].lower() == "switch":
                complete = self.patternSwitch(pattern, self.jobLoopCount)
            elif pattern["class"].lower() == "control":
                self.pushNewJob()
            else:
                print("jobStart: ERROR unknown class " + pattern["class"])
                time.sleep(1)
                
            # Complete - 0 indicates that the job's jobLoopCount expired
            if complete == 0:
                if (self.jobElement + 1) >= self.jobMax:
                    self.jobElement = 0
                    if jobLoop > 0:
                        jobLoop -= 1
                else:
                    self.jobElement += 1 
                
        return

     

    ############################################################################
    # Method: pushPrevActionCB() - Callback to Select next job
    #
    # Callback to Select next job
    ############################################################################
    def pushPrevActionCB(self, event=None):
        self.jobDirection = int(-1)
        self.pushNewJob()
        #self.sensePrevPattern([0,0,255])  # Print arrow
        return
    
    
    ############################################################################
    # Method: pushPrevActionCB() - Callback to Select previous job
    #
    # Callback to Select previous job
    ############################################################################
    def pushNextActionCB(self, event=None):
        self.jobDirection = int(1)
        self.pushNewJob()
        #self.senseNextPattern([255,0,0]) # print arrow
        return


    def pushNewJob(self):
        myJobElement = self.jobElement + self.jobDirection
        
        if myJobElement < 0:
            myJobElement = self.jobMax - 1
        elif myJobElement >= self.jobMax:
            myJobElement = 0
            
        self.jobElement = myJobElement
        self.jobSet()
        return
    
    
    
    

    ############################################################################
    # Method: boxConfigRefreshCB() - Callback to address refresh and pause
    #
    # Callback to address refresh and pause
    ############################################################################
    def boxConfigRefreshCB(self, event):      
        if event.direction == "middle":
            if event.action == "pressed": # trigger start
                self.jobSenseHide([0,0,0])
                
                if self.jobPause == False:
                    self.jobPause = True
                    for y in range (1, 7):
                       self.sense.set_pixel (1, y, 0xff, 0x00, 0x00)                
                       self.sense.set_pixel (2, y, 0xff, 0x00, 0x00)                
                       self.sense.set_pixel (5, y, 0xff, 0x00, 0x00)                
                       self.sense.set_pixel (6, y, 0xff, 0x00, 0x00)                
                else:
                    self.jobPause = False
                    self.jobSenseHide([0,0,0])
                    self.sense.show_letter(self.jName, self.jNameColor)
                    
 


   
    ############################################################################
    # Method: jobSenseHide() - Clear or hide part of the LED display
    #
    # Clear or hide part of the LED display
    ############################################################################
    def jobSenseHide(self, color):
        if self.sense:
            for x in range (0, 8):
                for y in range (1, 8):
                    self.sense.set_pixel (x, y, color)                
        return


    ############################################################################
    # Method: triggerSet() - display trigger pattern
    #
    # Display trigger pattern
    ############################################################################
    def triggerSet(self, color):
        self.jobSenseHide([0,0,255])
        for x in range (2, 6):
            for y in range (2, 6):
                self.sense.set_pixel (x, y, color)



    ############################################################################
    # Method: jobSenseLine() - display line pattern
    #
    # Display trigger pattern
    ############################################################################
    def jobSenseLine(self, color):
        for x in range (0, 8):
           self.sense.set_pixel (x, 4, color)                





        

    ############################################################################
    # Method: jobDebug() - A useless debug function
    #
    # A useless debug function
    ############################################################################
    def jobDebug(self):
        print ("jobListTest ")
        print ("  jobElement      " + repr(self.jobElement))
        print ("  jobMax          " + repr(self.jobMax))
        print ("  jobList         " + repr(self.jobList))
        print ("  jobTask         " + repr(self.jobTask))
        print ("  jobPause        " + repr(self.jobPause))
        print ("  jobRest         " + repr(self.jobRest))
        print ("  jobDirection    " + repr(self.jobDirection))

        print ("  jName           " + repr(self.jName))
        print ("  jNameColor      " + repr(self.jNameColor))

        print ("  jobSetCount     " + repr(self.jobSetCount))
        print ("  jobLoopCount    " + repr(self.jobLoopCount))
        return


if True:
    
    ############################################################################
    # Method: lightOakMain() - Used to debug this class
    #
    # Example: Just execut this script as main to invoke this function
    ############################################################################
    def jobListTest():


        job = jobList() 

        
        print ("Bye")
        return

    if __name__ == "__main__":
        jobListTest()



