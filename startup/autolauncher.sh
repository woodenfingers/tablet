#!/bin/bash

# Edit /etc/rc_local
# Add the following:
# /home/pi/ES/autolauncher.sh > /home/pi/ES/logs/rc_local.log &

#startPath=/home/pi/ES
#startProgram="chickenBarTest.py"
#startProgram="chickenBar.py"

#startPath=/home/rellis/spaceBar
#startProgram="lightBar.py"



echo `date`

############################################################

startPath=/home/pi/git/tablet/tShutdown 
startProgram="shutdownMan.py"

echo starting /usr/bin/python3 $startPath/$startProgram
/usr/bin/python3 $startPath/$startProgram  &
ps -elf | grep $startProgram 

#echo starting /usr/bin/python3 $startPath/$startProgram
#/usr/bin/python3 $startPath/$startProgram > $startPath/log/${startProgram%.*}.txt &
#ps -elf | grep $startProgram > $startPath/log/${startProgram%.*}.txt
#echo `ps -elf | grep $startProgram`


############################################################

startPath=/home/pi/git/tablet/tButtonMan 
startProgram="buttonMan.py"

echo starting /usr/bin/python3 $startPath/$startProgram
/usr/bin/python3 $startPath/$startProgram &
ps -elf | grep $startProgram 
echo `ps -elf | grep $startProgram`

#echo starting /usr/bin/python3 $startPath/$startProgram
#/usr/bin/python3 $startPath/$startProgram > $startPath/log/${startProgram%.*}.txt &
#ps -elf | grep $startProgram > $startPath/log/${startProgram%.*}.txt
#echo `ps -elf | grep $startProgram`


############################################################

#startPath=/home/pi/git/tablet/lightBarXXX
#startProgram="lightBar.py"

#echo starting /usr/bin/python3 $startPath/$startProgram
#/usr/bin/python3 $startPath/$startProgram > $startPath/log/${startProgram%.*}.txt &
#ps -elf | grep $startProgram > $startPath/help/${startProgram%.*}.txt
#echo `ps -elf | grep $startProgram`
