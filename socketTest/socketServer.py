#!/usr/bin/python3

import socket

from myChannel import myChannel
#from consIn import consIn

def main():
    #cons=consIn()
    #ch = cons.getch()
    #print(str(ch))


    server = myChannel()   
    server.serverDeamon02()
    print ('Bye - Server Died')
    
if __name__ == '__main__':
    main()