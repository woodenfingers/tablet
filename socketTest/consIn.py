#!/usr/bin/python3

################################################################################
# consIn - getch and nonblocking getch
#
# Copyright RHE 2019
#
# Code fragments sourced in from:
#    https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
#    http://code.activestate.com/recipes/134892/
#
# Other license:
# Attribution-NonCommercial-ShareAlike 3.0 United States (CC BY-NC-SA 3.0 US)
#  For non comercial use 
#  Image credits to Making Games with Python & Pygame - Albert Sweigart
#
# 19-05-27 - rhe - written 
################################################################################


################################################################################
# class consIn: Helper getch support
# windows _UNTESTED_
################################################################################
class consIn:

    def __init__(self):
        try:
            import msvcrt
            print ('!!! Windows host - untested')
            self.getch   = self.getchWindows
            self.getchNB = self.getchWindowsNoBlock
        except ImportError:
            import sys, select, tty, termios
            self.getch   = self.getchLinux
            self.getchNB = self.getchLinuxNoBlock

     #def __call__(self): return self.impl()
 
    ############################################################################
    # method getch() - get char from console - Blocking
    ############################################################################
    def getch(self):
        return self.getch()
 

    ############################################################################
    # method getche() - get char from console w/echo - Blocking
    ############################################################################
    def getche(self):
        ch = self.getch()
        print(ch)
        return ch

    ############################################################################
    # method getchNB() - get char from console - Non-Blocking
    ############################################################################
    def getchNB(self):
        print('!!! getchNB() called')
        return self.getchNB()

    ############################################################################
    # method getcheNB() - get char from console w/echo - Non-Blocking
    ############################################################################
    def getcheNB(self):
        ch = self.getchNB()
        if ch != None:
            print(ch)
        return ch


    ############################################################################
    # method getchWindows() - windows getch _UNTESTED_
    ############################################################################
    def getchWindows(self):
        import msvcrt
        print('!!! getchWindows() called - Untested')
        return msvcrt.getch()


    ############################################################################
    # method getchWindowsNoBlock() - windows getch _UNTESTED_
    ############################################################################
    def getchWindowsNoBlock(self):
        import msvcrt
        print('!!! getchWindowsNoBlock() called - Untested')
        return msvcrt.kbhit()()


    ############################################################################
    # method getchLinux() - linux getch 
    ############################################################################
    def getchLinux(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


    ############################################################################
    # method isData() - getchLinuxNoBlock helper 
    ############################################################################
    def isData(self):
        import sys, select, tty, termios
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


    ############################################################################
    # method getchLinuxNoBlock() - linux getch 
    ############################################################################
    def getchLinuxNoBlock(self):
        import sys, select, tty, termios
        #print('!!! getchLinuxNoBlock() called')
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            ch = None
            for x in range(0, 1):
                if self.isData():
                    ch = sys.stdin.read(1)
                    #print (str(x)+' '+' '+str(ch))
                    break
                #else:
                #    print(t)
        except:
            print('ERROR: Ubnable to set tty.setcbreak')
            exit(1)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            return ch
            

        




################################################################################
def main ():
    import time
    cons=consIn()   

    maxCount = 5

    print('!!! main() for _Cons()')

    print ("Test getch blocking - press any key")
    for x in range(0, maxCount):
        ch = cons.getch()
        print ('    Test getch blocking '+str(x)+'  Got: '+str(ch))

    print ("Test getche  blocking - press any key")
    for x in range(0, maxCount):
        ch = cons.getche ()
        print ('    Test getche  blocking '+str(x)+' Got: '+str(ch))



    print ("Test getchNB non-blocking - press any key")
    t = 1
    for x in range(0, maxCount):
        ch = None

        while ch is None:    
            ch = cons.getchNB()
            if ch != None:
               print ('    Test getchNB non-blocking '+str(x)+' Got: '+str(ch)+' '+str(t))

            #elif t & 0xffff == 0x1000:
            #    print (t)
            t += 1
        
    print ("Test getcheNB non-blocking - press any key")
    t = 1
    for x in range(0, maxCount):
        ch = None
        while ch is None:
        
            ch = cons.getcheNB()
            if ch != None:
               print ('    Test getcheNB non-blocking '+str(x)+' Got: '+str(ch)+' '+str(t))

            #elif t & 0xffff == 0x1000:
            #    print (t)
            t += 1
        
   
    print ("Test ing done")
    

if __name__ == '__main__':
    main()


