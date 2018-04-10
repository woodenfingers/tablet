#!/usr/bin/env python

################################################################################
# dancePat class
#
# Copyright RHE 2018
#
# 18-03-08 - rhe - written 
#
################################################################################


    

################################################################################
# Class dancePat
################################################################################
class dancePat():
    ############################################################################
    # Class constructor
    # Example: val = dancePat()
    ############################################################################
    def __init__ (self):

        
        self.begPat = (0b10101010, 1.75, 0b00000000,  .25)
        self.endPat = (0b00000000, 0)
        
        self.waltz = {
                "class" : "dance",
                "style" : ("Ballroom"),                                                                                 
                "name"  : ("Waltz"),
                "qName" : ("W"),
                "color" : (0x77, 0x77, 0x77),
                "bpm"   : (84, 90), # 84 - 90
                "bar"   : (3),
                "mask"  : (0xff),
                "begX"   : self.begPat,
                "pat"   : (0b01000000, 1,
                           0b01100000, 1,
                           0b01110000, 1,
                           0b00100000, 1,
                           0b00110000, 1,
                           0b00111000, 1,                
                           0b00010000, 1,
                           0b00011000, 1,
                           0b00011100, 1,                
                           0b00001000, 1,
                           0b00001100, 1,
                           0b00001110, 1),
                "step"  : "123123123123",
                "endX"   : self.endPat
            }

        self.vWaltz = {
                "class" : "dance",
                "style" : ("Ballroom"),                                                                                 
                "name"  : ("Vienesse Waltz"),
                "qName" : ("V"),
                "bpm"   : (174, 180),
                "bar"   : (3),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b01000000, 1,
                           0b01100000, 1,
                           0b01110000, 1,
                           0b00100000, 1,
                           0b00110000, 1,
                           0b00111000, 1,                
                           0b00010000, 1,
                           0b00011000, 1,
                           0b00011100, 1,                
                           0b00001000, 1,
                           0b00001100, 1,
                           0b00001110, 1),               
                "step"  : "123223323423",
                "end"   : self.endPat
            }

        self.foxTrot = {
                "class" : "dance",
                "style" : ("Ballroom"),                                                                                 
                "name"  : ("Foxtrot"),
                "qName" : ("F"),
                "bpm"   : (112, 120),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000110, 1,
                           0b00011000, 1,
                           0b00100000,  .5,
                           0b01000000,  .5),              
                "step"  : "SSQQ",
                "end"   : self.endPat
            }

        self.quickstep = {
                "class" : "dance",
                "style" : ("Ballroom"),                                                                                 
                "name"  : ("Quickstep"),
                "qName" : ("Q"),
                "bpm"   : (200, 208),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000110, 1,
                           0b00011000, 1,
                           0b00100000,  .75,
                           0b01000000,  .75),              
                "step"  : "SSQQ",
                "end"   : self.endPat
            }

        self.tango = {
                "class" : "dance",
                "style" : ("Ballroom"),                                                                 
                "name"  : ("Tango"),
                "qName" : ("T"),
                "bpm"   : (120, 140),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000010, 1,
                           0b00000100, 1,
                           0b00001000, 1,
                           0b00110000, 2,
                           0b01000000,  .5),               
                "step"  : "SSS>Q",
                "end"   : self.endPat
            } 

        self.chaChaCha = {
                "class" : "dance",
                "style" : ("Ballroom"),                                                 
                "name"  : ("Cha Cha Cha"),
                "qName" : ("C"),
                "bpm"   : (120, 128),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : (0b10101010, 1.75,
                           0b00000000,  .25),
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
            }

        self.rumba = {
                "class" : "dance",
                "style" : ("Ballroom"),                                 
                "name"  : ("Rumba"),
                "qName" : ("R"),
                "bpm"   : (100, 108),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000110, 1,
                           0b00001000,  .5 ,
                           0b00010000,  .5),
                "step"  : "SQQ",
                "end"   : self.endPat
            }

        self.rumbaVal = {
                "class" : "dance",
                "style" : ("Ballroom"),                                 
                "name"  : ("Rumba V"),
                "qName" : ("r"),
                "bpm"   : (100, 108),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000010,  .5,
                           0b00000100,  .5,
                           0b00011000, 1),
                "step"  : "QQS",
                "end"   : self.endPat
            }

        self.samba = {
                "class" : "dance",
                "style" : ("Ballroom"),                                 
                "name"  : ("Samba"),
                "qName" : ("s"),
                "bpm"   : (96, 104),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
            }

        self.jive = {
                "class" : "dance",
                "style" : ("Ballroom"),                                 
                "name"  : ("Jive"),
                "qName" : ("J"),
                "bpm"   : (168, 184),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
            }

        self.pasoDoble = {
                "class" : "dance",
                "style" : ("Ballroom"),                                 
                "name"  : ("Paso Doble"),
                "qName" : ("P"),
                "bpm"   : (168, 184),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
            }
        
        
        self.lindyHop = {
                "class" : "dance",
                "style" : ("Swing"),                                 
                "name"  : ("Lindy Hop"),
                "qName" : ("L"),
                "bpm"   : (168, 184),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
            }

        self.charleston = {
                "class" : "dance",
                "style" : ("Swing"),                                 
                "name"  : ("Charleston"),
                "qName" : ("C"),
                "bpm"   : (200, 290),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "end"   : self.endPat
            }

        self.balboa = {
                "class" : "dance",
                "style" : ("Swing"),                                 
                "name"  : ("Balboa"),
                "qName" : ("B"),
                "bpm"   : (175, 340),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
            }
        
        self.ecSwing = {
                "class" : "dance",
                "style" : ("Swing"),                                 
                "name"  : ("EC Swing"),
                "qName" : ("E"),
                "bpm"   : (120, 250),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
            }

        self.blues = {
                "class" : "dance",
                "style" : ("Swing"), 
                "name"  : ("Blues Dance"),
                "qName" : ("B"),
                "bpm"   : (20, 75),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "end"   : self.endPat
            }

        self.aTango = {
                "class" : "dance",
                "style" : ("Tango"), 
                "name"  : ("Tango Argentino"),
                "qName" : ("A"),
                "bpm"   : (80, 160),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
            }

        self.nTango = {
                "class" : "dance",
                "style" : ("Tango"), 
                "name"  : ("Tango Nuevo"),
                "qName" : ("N"),
                "bpm"   : (40, 160),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
            }

        self.milonganame = {
                "class" : "dance",
                "style" : ("Tango"), 
                "name"  : ("Milonga"),
                "qName" : ("M"),
                "bpm"   : (150, 240),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
            }

        self.salsa  = {
                "class" : "dance",
                "style" : ("Latin"), 
                "name"  : ("Salsa"),
                "qName" : ("S"),
                "bpm"   : (180, 300),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
            }

        self.merenge = {
                "style" : ("Latin"), 
                "class" : "dance",
                "name"  : ("Merenge"),
                "qName" : ("m"),
                "bpm"   : (130, 200),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
            }

        self.bachata = {
                "class" : "dance",
                "style" : ("Latin"), 
                "name"  : ("Bachata"),
                "qName" : ("B"),
                "bpm"   : (90, 200),
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : self.begPat,
                "pat"   : (0b00000000, 1,
                           0b00000000, 1),
                "step"  : "  ",
                "end"   : self.endPat
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
    def dancePatTest():
        myDance = dancePat() 
        myDanceSet = [myDance.foxTrot, myDance.waltz, myDance.vWaltz, myDance.tango]
        print ("myDanceSet  " + repr(myDanceSet))
        print ("\nmyDanceSet0 " + repr(myDanceSet[0]))
        print ("\nmyDanceSet1 " + repr(myDanceSet[1]))
        print ("\nmyDanceSet2 " + repr(myDanceSet[2]))
          
    
        print ("\ndancePatTest: Bye")
        return

        
    if __name__ == "__main__":
        dancePatTest()





