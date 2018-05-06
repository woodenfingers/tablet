#!/usr/bin/env python

################################################################################
# hwMgrDef class
#
# Copyright RHE 2018
#
# 18-05-04 - rhe - ported 
#
################################################################################

   


################################################################################
# Class hwMgrDef
################################################################################
class hwMgrDef():
    ############################################################################
    # Class constructor
    # Example: myChase = hwMgrDef.chaserClass(device)
    #    device:
    #        relay4  - OUT: Relays 0-3 supported
    #                   IN: 
    #        relay8  - OUT: Relays 0-7 supported
    #                   IN: 
    #        Relay16 - OUT: Relays 0-15 supported
    #                   IN:
    ############################################################################
    def __init__ (self, hardwareDevice):


        self.tiggerPin=12
        self.shutdownPin=0

        self.color = {
            "off":    (  0,   0,   0),
            "red":    (255,   0,   0),
            "green":  (  0, 255,   0),
            "yellow": (255, 255,   0),
            "blue":   (  0,   0, 255)
            }       

        self.ioMgr = {
        #      GPIO,pin,   mask, TBD 
             0: (27, 13, 0x0001,  1),
             1: (22, 15, 0x0002,  2),
             2: ( 5, 29, 0x0004,  3),
             3: ( 6, 31, 0x0008,  4),
             4: (19, 35, 0x0010,  5),
             5: (26, 37, 0x0020,  6),
             6: (20, 38, 0x0040,  7),
             7: (16, 36, 0x0080,  8),
             8: (12, 32, 0x0100,  9),
             9: ( 7, 26, 0x0200, 10),
            10: (18, 12, 0x0400, 11),
            11: (15, 10, 0x0800, 12),
            12: (14,  8, 0x1000, 13),
            13: (17, 11, 0x2000, 14),
            14: (13, 33, 0x4000, 15),
            15: (21, 40, 0x8000, 16)
            }

        #             ioBed opEnd  pMask   invrt     
        ioBoardCfg = {
             'relay4'  : (0,    4, 0x0f,   False),
             'relay8'  : (0,    8, 0xff,   False),
             'relay8i' : (0,    8, 0xff,   True ),
             'relay16' : (0,   16, 0xffff, False), 
             'aHat'    : (0,    3, 0x3,    False),
            }
        try:
            cfg = ioBoardCfg[hardwareDevice]
            self.hwId = hardwareDevice
            self.ioBeg = cfg[0]    
            self.ioEnd = cfg[1]    
            self.oMask = cfg[2]
            self.invrt = cfg[3]
        except:
            print("WARNING: Unsupported device " + repr(hardwareDevice) + " - Ignoring HW setup")
            self.hwId = "ERROR"
            self.ioBeg = 0    
            self.ioEnd = 0    
            self.oMask = 0
            self.invrt = False
            print ("self.invrt " + self.invrt)
            return
        

        return


