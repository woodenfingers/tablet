#!/usr/bin/env python

################################################################################
# test
#
# Copyright RHE 2018
#
# 18-04-09 - rhe - written 
#
################################################################################

import time
import sys
sys.path.append('../barOak')

import platform





################################################################################
# Main Do something
################################################################################
def main():
    myPlatform = platform.node()
    print ("platform " + repr(myPlatform))    
    print ("Bye.")
    return True


       

if __name__ == "__main__":
    main()


    


