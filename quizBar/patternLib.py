#!/usr/bin/python3


################################################################################
# patterLib
#    Simple pattern collection class
#
# Copyright RHE 2018
#
# 18-02-08 - rhe - updated patterns 
# 18-02-08 - rhe - written 
#
################################################################################

    

################################################################################
# Class patternLib - collection of lightBar patterns
################################################################################
class patternLib():
    ############################################################################
    # Class constructor
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
                           0b01100000, 1,                
                           0b11000000, 1,                
                           0b10000000, 1),              
                "end"   : (0b00000000, 0)
                }

        self.chasePattern21 = {
                "class" : "switch",
                "name"  : ("switch back 9"),
                "qName" : ("s"),
                "color" : (0xff, 0x0f, 0xf0),
                "bpm"   : (100,1000), #
                "bar"   : (4),
                "mask"  : (0xff),
                "beg"   : (0b00000000, 1),
                "pat"   : (0b00000110, 1,
                           0b00001100, 1,
                           0b00011000, 1,
                           0b00110000, 1,                
                           0b01100000, 1),              
                "end"   : (0b00000000, 0)
                }

        self.slowDown = {
                "qName" : ("A"),
                "color" : (0x00, 0xff, 0x00),
                "bpm"   : (100,1000), #
                "mask"  : (0b11110111),
                "pat"   : (0b00000100,  .2,
                           0b00010010,  .4,
                           0b01011100,  .6,
                           0b00111000,  .8,
                           0b01010010, 1,
                           0b00110000, 1.2,                
                           0b01001100, 1.4,
                           0b00000100, 1.6,
                           0b00010010, 1.8,
                           0b01011100, 2.0,
                           0b00111000, 2.2,
                           0b01010010, 2.4,
                           0b00110000, 2.8,                
                           0b01001100, 3.0,                
                           0b10011010, 4.0,              
                           0b10011011, 4.0),            
                "end"   : (0b00000000, .1)
                }
        
        self.correctLight = {
                "qName" : ("C"),
                "color" : (0x00, 0xff, 0x00),
                "bpm"   : (100,1000), #
                "mask"  : (0b11111111),
                "end"   : (0b00000001, .1)
                }

        self.inCorrectLight = {
                "qName" : ("X"),
                "color" : (0xff, 0x00, 0x00),
                "bpm"   : (100,1000), #
                "mask"  : (0b11111111),             
                "end"   : (0b10000000, .1)
                }

        self.allOffLight = {
                "end"   : (0b00000000, .1)
                }
        

        return


                                   
            

    ############################################################################
    # method: __str__()
    ############################################################################
    def __str__(self):
        return "patternLib"










    


