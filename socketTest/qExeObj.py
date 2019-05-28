#!/usr/bin/python3

################################################################################
# qThreads - quize Threads
#
# Copyright RHE 2019
#
# Code fragments sourced in from:
#    https://pythonprogramming.net/buffering-streaming-data-sockets-tutorial-python-3/?completed=/sockets-tutorial-python-3/
#    https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
#
# 19-05-27 - rhe - written 
################################################################################

import socket
import time
# BAD from _threads import _threads
import threading


class qExeObj():
    
    # clientIndex = 0 is always a client App. Otherwise its a server app
    def __init__(self, clientIndex, conn, addr):
        self.stop        = False
        self.stopped     = False
        self.clientIndex = str(clientIndex)
        self.conn        = conn
        self.addr        = addr
        
        # fixed formatting header
        self.msgSize = 4
        self.cmdSize = 1
        self.hdrSize = self.msgSize + self.cmdSize
        #msg = self.msgCreate('P','Hello World')
        #print (msg)
        #print (self.msgCmd(msg))
        #print (self.msgLen(msg))
        #print (self.msgMsg(msg))
        self.serverGreeting = ''
        self.pingTx = 0
        self.pingRx = 0

        #print('onNewClient clientsocket '+str(self.conn))
        #print('onNewClient addr         '+str(self.addr))
        print('__init__ '+self.clientIndex)
        if clientIndex == 0:
            self.thrd = threading.Thread(target=self.clientApp, args=(self.conn,self.addr))
        else:    
            self.thrd = threading.Thread(target=self.serverApp, args=(self.conn,self.addr))
        return 
            
            
    ############################################################################
    # method ping() - send ping
    ############################################################################
    def start(self):
        print('start '+self.clientIndex)
        self.thrd.start()


    ############################################################################
    # method kill() - kill thread
    ############################################################################
    def kill(self):
        print('kill '+self.clientIndex)
        self.stop = True
        for t in range(1, 1000):
            if self.stopped is True:
                break
            sleep(0.01)
        return self.stopped


    ############################################################################
    # method serverApp() - run core 
    ############################################################################
    def serverApp(self, conn, addr):
        print('serverApp '+self.clientIndex)
        self.msgSend(self.conn, 'M','rPiQuiz')
        while True:
            if self.stop is True:
                break
            self.parseMsg(self.msgReceive(conn))
        
        # Thread is ending
        self.stopped = True
        self.conn.close()



    ############################################################################
    # method clientApp() - run core 
    ############################################################################
    def clientApp(self, server, addr):
        print('clientApp '+self.clientIndex)
        while True:
            if self.stop is True:
                break
            self.parseMsg(self.msgReceive(server))
            

        # Thread is ending
        self.stopped = True
        self.conn.close()

    def parseMsg(self, msg):
        myCmd  = self.msgCmd(msg)
        myData = self.msgMsg(msg)
        # print('parseMsg '+self.clientIndex+' '+myCmd+' '+myData)
        
        if myCmd == 'M':
            self.serverGreeting = myData
        elif myCmd == 'P':
            self.msgSend(self.conn, 'R', myData)
        elif myCmd == 'R':
            self.pingRx += 1
        else:
            print('parseMsg '+self.clientIndex+' '+myCmd+' '+myData+' UNKNOWN')
            
        


    ############################################################################
    # method ping() - send ping
    ############################################################################
    def ping(self):
        self.pingTx += 1
        print('ping '+self.clientIndex+' '+str(self.pingTx)+' '+str(self.pingRx))
        self.msgSend(self.conn, 'P', str(time.time()))
        

    ############################################################################
    # method msgCreate() - Send and recieve and close seeion each time
    # Messages
    # <len>p<msg>      - ping - seng ping with message
    # <len>r<msg>      - ping - return message uses recieved client
    # <len>B<1-n>      - Button Pressed
    # <len>L<1-8>      - Light On
    # <len>l<1-8>      - Light Off
    # <len>P<11111111> - light pattern
    # <len>A<msg>      - ACK command
    # <len>N<msg>      - NAK command
    # <len>M<msg>      - Just a message
    ############################################################################
    def msgCreate(self, cmd, msg):
        hdrFmt='{:<'+str(self.msgSize)+'}'
        cmdFmt='{:<'+str(self.cmdSize)+'}'
        fmtMsg=hdrFmt.format(str(len(msg)))+cmdFmt.format(str(cmd))+str(msg)
        return fmtMsg

    ############################################################################
    # method msgCmd() - return a message command
    ############################################################################
    def msgCmd(self, msg):
        return msg[self.msgSize:self.hdrSize]
    
    ############################################################################
    # method msgLen() - return a message length
    ############################################################################
    def msgLen(self, msg):
        if len(msg) < self.msgSize:
            print ('ERROR: Msg too small '+str(len(msg)))
        return int(msg[0:self.msgSize])

    ############################################################################
    # method msgLen() - return a message content
    ############################################################################
    def msgMsg(self, msg):
        return msg[self.hdrSize:]



    ############################################################################
    # method msgReceive() - receive a variable length message from socket
    # Message contains an embedded command
    ############################################################################
    def msgReceive(self, soc):
        fullMsg = ''
        newMsg  = True
        msglen  = self.hdrSize # first pass grab the whole header
        while True:
            msg = soc.recv(msglen)
            fullMsg += msg.decode("utf-8")
            if newMsg is True:
                # Get message header
                if len(msg) > self.hdrSize:
                    # We did not get the whole header
                    msglen -= len(msg)
                else:
                    # Full header was recieved. Now,get the rest of the message
                    msglen = self.msgLen(fullMsg)
                    newMsg = False
            else:
                # Get message content
                msglen = max(msglen-len(msg), 0)

   
            if msglen == 0:
                # Full message was received.
                return fullMsg



    ############################################################################
    # method msgSend() - format command / message and send to a socket
    ############################################################################
    def msgSend(self, soc, cmd, msg):
        sMsg = self.msgCreate(str(cmd),msg)
        return soc.send(bytes(sMsg, "utf-8"))






    """
    def onNewClient(self, clientsocket,addr):
        print('onNewClient clientsocket '+str(clientsocket))
        print('onNewClient addr         '+str(addr))
        self.msgSend(clientsocket, 'M','rPiQuiz')
        while True:
            time.sleep(7)
            print('Ping client')
            self.msgSend(clientsocket, 'P', str(time.time()))
        clientsocket.close()
    """    
