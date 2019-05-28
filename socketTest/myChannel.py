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
import threading

from qExeObj import qExeObj


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
            
        self.myQApp      = None
        
        self.clientQThd  = []
        self.clientConn  = []
        self.clientAddr  = []
        self.clientCount = 1

        self.serverQThd  = []
        self.serverConn  = []
        self.serverAddr  = []

    def quizThread(self):
        print('!!! quizThread() starting')
        time.sleep(7)
        while True:
            t = 0
            for q in self.clientQThd:
                time.sleep(1)
                q.ping()
                t += 1
            time.sleep(max(10-t, 1))
            

    
    
    ############################################################################
    # method closeClientConnections() - close all client connections 
    # Close all client connections known by the server connections
    # Call during start of server just incase its a restart
    ############################################################################
    def closeClientConnections(self):
        # kill and delete thread classes
        print('!!! Server is closing all client connections')
        for q in self.clientQThd:
            q.kill()
            del q
        self.clientQThd.clear()

        for c in self.clientConn:
            c.close()
        self.clientConn.clear()
        self.clientAddr.clear()
        self.clientCount = 1



    ############################################################################
    # method closeServerConnections() - close all server connections 
    # Close all client connections known by the server connections
    # Call during start of client just incase its a restart
    ############################################################################
    def closeServerConnections(self):
        # kill and delete thread classes
        print('!!! Client is closing all server connections')
        for q in self.serverQThd:
            q.kill()
            del q
        self.serverQThd.clear()

        for c in self.serverConn:
            c.close()
        self.serverConn.clear()
        self.serverAddr.clear()



    def serverDeamon02(self):
        if self.serverOK is False:
            print('ERROR: No starting server on '+self.myServerHost)
            print('       You are on '+socket.gethostname())
            exit(1)
        print('!!! serverDeamon02: Starting server on '+str(self.myIP)+' Port '+str(self.port))

        self.closeClientConnections()

        

        # create the socket
        # AF_INET == ipv4
        # SOCK_STREAM == TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.bind((self.myIP, self.port))

        s.listen(10)
        first = True
        while True:
            # now our endpoint knows about the OTHER endpoint.
            clientsocket, address = s.accept()
            s.setblocking(1)     # prevent client timeout from happening
            print('Connection from '+str(address)+' has been established!')
            if first is True:
                self.myQApp = threading.Thread(target=self.quizThread)
                self.myQApp.start()
                first = False
                
            q = qExeObj(self.clientCount, clientsocket, address)
            self.clientCount += 1
            self.clientQThd.append(q)
            
            self.clientConn.append(clientsocket)
            self.clientAddr.append(address)
            q.start()
            #thread.start_new_thread(onNewClient,(clientsocket,address))
            
        s.close()
        return



    ############################################################################
    # method client01() - Send and recieve and close session each time
    # See serverDeamon01()
    ############################################################################
    def client02(self):
        print('!!! Starting client02 on '+str(self.myIP)+' Port '+str(self.port))
        self.closeServerConnections()
        
        # create the socket
        # AF_INET == ipv4
        # SOCK_STREAM == TCP
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self.myIP, self.port))

        q = qExeObj(0, server, self.myIP)
        self.serverQThd.append(q)
        self.clientConn.append(server)
        self.clientAddr.append(self.myIP)

        q.start()









    





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