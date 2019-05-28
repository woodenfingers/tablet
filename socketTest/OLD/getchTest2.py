class _Cons:
    """Gets a single character from standard input.  Does not echo to the
screen."""
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
 
    def getch(self):
        return self.getch()
 
    def getchNB(self):
        print('!!! getch() called')
        return self.getchNB()

    def getchWindows(self):
        import msvcrt
        print('!!! getchWindows() called - Untested')
        return msvcrt.getch()

    def getchWindowsNoBlock(self):
        import msvcrt
        print('!!! getchWindowsNoBlock() called - Untested')
        return msvcrt.kbhit()()


    def getchLinux(self):
        import sys, tty, termios
        print('!!! getchLinux() called')
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def isData(self):
        import sys, select, tty, termios
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

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
            

        




def main ():
    import time
    cons=_Cons()   
    
    print('!!! main() for _Cons()')
    t = 1
    while True:
        #ch = cons.getch()
        ch = cons.getchNB()
        if ch != None:
            print ('!!! Got: '+str(ch)+' '+str(t))
            exit()
        elif t & 0xfff == 0x100:
            print (t)
        #time.sleep(1)
        t += 1 
    
    #ch = cons.getch()  

if __name__ == '__main__':
    main()


