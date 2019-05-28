#!/usr/bin/python3

################################################################################
# myChannel - socket channel
#
# Copyright RHE 2019
#
# Code fragments sourced in from:
#    https://pythonprogramming.net/buffering-streaming-data-sockets-tutorial-python-3/?completed=/sockets-tutorial-python-3/
#
# Other license:
# Attribution-NonCommercial-ShareAlike 3.0 United States (CC BY-NC-SA 3.0 US)
#  For non comercial use 
#  Image credits to Making Games with Python & Pygame - Albert Sweigart
#
# 19-05-27 - rhe - written 
################################################################################

import socket
import time
import pickle


class myChannel():
    
    def __init__(self, ip='192.168.4.1', port=1234):
        self.myIP = ip
        #self.myIP = socket.gethostname()
        self.myServerHost = 'rpiQuizMaster'
        self.port = port

        if self.myServerHost == socket.gethostname():
            print ('Running on '+str(self.myServerHost))
            self.serverOK = True
        else:
            print ('Not '+str(self.myServerHost))
            self.serverOK = False
            
        # fixed formatting header
        self.msgSize = 4
        self.cmdSize = 1
        self.hdrSize = self.msgSize + self.cmdSize
        msg = self.msgCreate('P','Hello World')
        print (msg)
        print (self.msgCmd(msg))
        print (self.msgLen(msg))
        print (self.msgMsg(msg))

    
    





    def serverDeamon02(self):
        if self.serverOK is False:
            print('ERROR: No starting server on '+self.myServerHost)
            print('       You are on '+socket.gethostname())
            exit(1)
        print('!!! serverDeamon02: Starting server on '+str(self.myIP)+' Port '+str(self.port))

        # create the socket
        # AF_INET == ipv4
        # SOCK_STREAM == TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.bind((self.myIP, self.port))

        s.listen(10)


        while True:
            # now our endpoint knows about the OTHER endpoint.
            clientsocket, address = s.accept()
            print('Connection from '+str(address)+' has been established!')

            self.msgSend(clientsocket, 'M','rPiQuiz')
            
            while True:
                time.sleep(7)
                print('Ping client')
                self.msgSend(clientsocket, 'P', str(time.time()))
                
            # clientsocket.close()
            return



    ############################################################################
    # method client01() - Send and recieve and close session each time
    # See serverDeamon01()
    ############################################################################
    def client02(self):
        print('!!! Starting client02 on '+str(self.myIP)+' Port '+str(self.port))
        # create the socket
        # AF_INET == ipv4
        # SOCK_STREAM == TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.myIP, self.port))

        while True:
            myMsg = self.msgReceive(s)
            print (str(myMsg))
        return










    
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
        return int(msg[0:self.msgSize])

    ############################################################################
    # method msgLen() - return a message content
    ############################################################################
    def msgMsg(self, msg):
        return msg[self.hdrSize]



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











    ############################################################################
    # method serverDeamon01() - Send and recieve and close session each time
    # See client01()
    ############################################################################
    def serverDeamon01(self):
        if self.serverOK is False:
            print('ERROR: No starting server on '+self.myServerHost)
            print('       You are on '+socket.gethostname())
            exit(1)
        print('!!! serverDeamon01: Starting server on '+str(self.myIP)+' Port '+str(self.port))

        # create the socket
        # AF_INET == ipv4
        # SOCK_STREAM == TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.bind((self.myIP, self.port))

        s.listen(10)


        while True:
            # now our endpoint knows about the OTHER endpoint.
            clientsocket, address = s.accept()
            print('Connection from '+str(address)+' has been established!')
            clientsocket.send(bytes("rPiQuiz", "utf-8"))
            clientsocket.close()


    ############################################################################
    # method client01() - Send and recieve and close session each time
    # See serverDeamon01()
    ############################################################################
    def client01(self):
        # create the socket
        # AF_INET == ipv4
        # SOCK_STREAM == TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print('!!! Starting client01 on '+str(self.myIP)+' Port '+str(self.port))

        s.connect((self.myIP, self.port))

        full_msg = ''
        while True:
            msg = s.recv(8)
            if len(msg) <= 0:
                break
            full_msg += msg.decode("utf-8")

        print(full_msg)
        return


def main():
    server = myChannel(server=True, port=1234)   
    server.serverDeamon()
    print ('Bye - Server Died')
    
if __name__ == '__main__':
    main()