#!/usr/bin/env python

################################################################################
# lightBar driver
#
# Copyright RHE 2018
#
# 18-02-08 - rhe - written 
#
################################################################################

    

################################################################################
# Class dancePat
################################################################################
class patternLib():
    ############################################################################
    # Class constructor
    # Example: val = dancePat()
    ############################################################################
    def __init__ (self):


        self.pattern00 = {
                "class" : "sequence",
                "name"  : ("Off"),
                "qName" : ("X"),
                "pat"   : (0b00000000, 1)            
                }

        self.pattern01 = {
                "class" : "sequence",
                "qName" : ("1"),
                "pat"   : (0b00000001, 1)              
                }

        self.pattern02 = {
                "class" : "sequence",
                "qName" : ("2"),
                "pat"   : (0b00000010, 1)              
                }

        self.pattern03 = {
                "class" : "sequence",
                "qName" : ("3"),
                "pat"   : (0b00000100, 1)              
                }

        self.pattern04 = {
                "class" : "sequence",
                "qName" : ("4"),
                "pat"   : (0b00001000, 1)              
                }

        self.pattern05 = {
                "class" : "sequence",
                "qName" : ("5"),
                "pat"   : (0b00010000, 1)              
                }

        self.pattern06 = {
                "class" : "sequence",
                "qName" : ("6"),
                "pat"   : (0b00100000, 1)              
                }

        self.pattern07 = {
                "class" : "sequence",
                "qName" : ("7"),
                "pat"   : (0b01000000, 1)              
                }

        self.pattern08 = {
                "class" : "sequence",
                "qName" : ("8"),
                "pat"   : (0b10000000, 1)              
                }

        self.chasePattern11 = {
                "class" : "sequence",
                "name"  : ("Chase 1"),
                "qName" : ("a"),
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



        self.chasePattern12 = {
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

        self.chasePattern13 = {
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



        self.chasePattern20 = {
                "class" : "switch",
                "name"  : ("switch back 9"),
                "qName" : ("s"),
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

        self.controlForever = {
                "class"      : "control",
                "name"       : ("forever"),
                "jobSetCount"  : -1,
                "jobLoopCount" : -1
                }
        self.controlOne = {
                "class"        : "control",
                "name"         : ("forever"),
                "jobSetCount"  : 1,
                "jobLoopCount" : 1
                }
        

        return


                                   
            

    def __str__(self):
        return "dancePat"


if True:
        
        
    ############################################################################
    # Method: lightOakMain() - Used to debug this class
    #
    # Example: Just execut this script as main to invoke this function
    ############################################################################
    def patternTest():
        pl = patLib() 
        myPatSet = [pl.pattern00, pl.pattern01, pl.pattern02, pl.pattern03, 
                    pl.pattern04, pl.pattern05, pl.pattern06, pl.pattern07,
                    pl.pattern08,
                    pl.chasePattern11, pl.chasePattern12, pl.chasePattern13, 
                    pl.chasePattern20]
        print ("myPatSet  " + repr(myPatSet))
        print ("\nmyPatSet0 " + repr(myPatSet[0]))
        print ("\nmyPatSet1 " + repr(myPatSet[1]))
        print ("\nmyPatSet2 " + repr(myPatSet[2]))
          
    
        print ("\npatternTest: Bye")
        return

        
    if __name__ == "__main__":
        patternTest()









    


