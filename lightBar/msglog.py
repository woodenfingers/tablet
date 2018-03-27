#!/usr/bin/env python

################################################################################
# msgLog class
#
# Copywright Tesfaye Firew 2018
#
# 18-02-18 - tkf - Module for logging messages
# 18-02-19 - tkf - Added logmsgMail class
# 19-03-01 - rhe - Added level support and embedded test 
#
################################################################################

import datetime
import time

# The following are needed for email support
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

################################################################################
# Class msglog
################################################################################
class msglog:

    ############################################################################
    # Class constructor
    # Example: logger = msglog.msglog (toConsole, toSense, filename, address)
    #    - toConsole - boolean value - display message to terminal if True
    #    - toSense - boolean value - display message to sense screen if True
    #    - filename - string - full pathname to file to write message to
    #    - address - string - address of text recipient to send message as text
    ############################################################################
    def __init__ (self, toConsole=True, toSense=False, filename="", address=""):

        self.txtmsgs = 0
        self.snsmsgs = 0

        self.toConsole = toConsole
        self.toSense = toSense
        self.toFs = False
        self.toText = False

        self.warningFlag = False

        if (address != ''):
            self.toText = True
            self.address = address

        if (filename != ''):
            self.filename = filename
            self.toFs = True

        return


    ############################################################################
    # Method: msgLogReset - Reset the message log file (the msglog object 
    #                       sholuld have been created with valid filename
    #                       argument)
    #
    # Example: msglog.msgLogReset ()
    ############################################################################
    def msgLogReset(self):
        if (self.toFs == False):
            return False

        try:
            self.fd = open (self.filename, "w+")
            self.fd.close ()
        except:
            if self.warningFlag == False:
                print("WARNING msgLogReset() could not open " + repr(self.filename))
                self.warningFlag = True
        return True


    ############################################################################
    # Method: msgWriteToFs - Write message to a file system
    #
    # The msglog object sholuld have been created with valid filename argument.
    # Message is appended to the end of the file. If it is needed to overwrite
    # previous content, call msgLogReset() before calling this method.
    #
    # Example: msglog.msgWriteToFs (msg)
    ############################################################################
    def msgWriteToFs(self, msg):
        if (self.toFs == False):
            return False

        try:
            self.fd = open (self.filename, "a+")
            self.fd.write (msg + "\r")
            self.fd.close()
        except:
            if self.warningFlag == False:
                print("WARNING msgWriteToFs() could not open " + repr(self.filename))
                self.warningFlag = True
        return
    

    ############################################################################
    # Method: msgWriteToSense - Write message to the HAT sensor
    #
    # Example: msglog.msgWriteToSense (msg)
    ############################################################################
    def msgWriteToSense(self, message):
        if self.toSense == True:
            self.sense.show_message(message)
            return 1
        else:
            return 0


    ############################################################################
    # Method: msgWriteToText - Send message as a text message
    #
    # Example: msglog.msgWriteToText (msg)
    ############################################################################
    def msgWriteToText(self, msg):
        if (self.toSense == False):
            return False

        if (self.txtmsgs == 0):
            print ("**** No text message support ****\n")

        self.txtmsgs += 1
        return True

    ############################################################################
    # Method: msgLogFormat - Format log message
    #
    # Example:
    #     msg = msglog.msgLogFormat (msg)
    ############################################################################
    def msgLogFormat(self, msg):
        msg = repr(time.ctime()) + " : " + msg
        return msg

    ############################################################################
    # Method: msgLog - Log message with timestamp
    #
    # Example:
    #     fd = msglog.msglog (toConsole, toSense, filename, address)
    #     fd.msgLog (msg)
    ############################################################################
    def msgLog(self, message):
        return self.logMsg1(0, message)

    
    def logMsg(self, message):
        return self.logMsg1(0, message)


    def logMsg1(self, level, message):
        istr = ""
        for x in range (0, level * 2):
            istr = istr + " "

        messagePad = istr + message
        messageFrm = self.msgLogFormat (messagePad)

        written = False
        if (self.toConsole == True):
            print (messageFrm)
            written = True

        if (self.toFs == True):
            self.msgWriteToFs (messageFrm)
            written = True


        # Only send level zero messages to text or sence
        if level == 0:
            if (self.toSense == True):
                self.msgWriteToSense (message)
                written = True

            if (self.toText == True):
                msgWriteToText (messageFrm)
                written = True

        return written


    def logClose(self):
        # Add log close support here
        return print("logClose()")

################################################################################
# Class msglogMail
################################################################################
class msglogMail:

    ############################################################################
    # Class constructor
    # Example: mlm = msglog.msglogMail (sName, sPasswd, subject, recipList)
    #    - sName - sender gmail user name
    #    - sPasswd - sender gmail user password
    #    - subject - mail subject
    #    - recipList - list of recipient addresses
    ############################################################################
    def __init__ (self, sName, sPasswd, subject, recipList):
        self.name = sName
        self.passwd = sPasswd
        self.subject = subject
        self.recipients = recipList

    ############################################################################
    # Method: msgMail - mail a log message
    # Example: mlm = msglogMail.msgMail (message, attachment)
    #    - message - message text to send
    #    - attachment - name of file to attach
    ############################################################################
    def msgMail(self, msg, attach):

        # Construct the mail header
        mail = MIMEMultipart()
        mail['From'] = self.name
        mail['To'] = ', '.join (self.recipients)
        mail['Subject'] = self.subject

        msg = msglog.msgLogFormat (msglog, msg)
        mail.attach (MIMEText (msg))

        # Attach if necessary
        if (attach != ''):
            part = MIMEBase ('application', 'octet-stream')
            part.set_payload (open (attach, 'rb').read())
            Encoders.encode_base64 (part)
            part.add_header ('Content-Disposition',
                'attachment; filename="%s"' % os.path.basename (attach))
            mail.attach (part)

        # Setup the mail service
        server = smtplib.SMTP ("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login (self.name, self.passwd)
        server.sendmail (self.name, self.recipients, mail.as_string())
        server.close()


if True:
    ############################################################################
    # Method: logMain() - Used to debug this class
    #
    # Example: Just execut this script as main to invoke this function
    # Note: The RPi sense hat is not testable here. However, it is testable via
    #       the ioak test since self.sense is defined.
    ############################################################################
    def logTest():
        logD = msglog(True, False, "./myDebugFile")
        #logD = msglog(True, False, "/mnt/gdrivefs/test/thisIsABadFileName.txt") 
        print ("logD.txtmsgs   " + repr(logD.txtmsgs))
        print ("logD.snsmsgs   " + repr(logD.snsmsgs))

        #print ("logD.fdIsOpen  " + repr(logD.fdIsOpen))
        print ("logD.toFs      " + repr(logD.toFs))
        print ("logD.toConsole " + repr(logD.toConsole)) 
        print ("logD.toSense   " + repr(logD.toSense))
        print ("logD.toText    " + repr(logD.toText))

        logD.logMsg("log.py: Debugging")
        
        logD.logMsg1(0, "level 0")
        logD.logMsg1(1, "level 1")
        logD.logMsg1(2, "level 2")
        logD.logMsg1(5, "level 5")

        fly=8
        logD.logMsg1(0, "fly:")
        logD.logMsg1(1, "my fly: " + repr(fly))

        logD.logMsg("Bye")

        return


    if __name__ == "__main__":
        logTest()