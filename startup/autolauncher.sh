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

startPath=/home/pi/git/tablet/tShutdown
startProgram="shutdownMan.py"

found=`ls $startPath/$startProgram`

if [ $? == "0" ]; then
    echo starting /usr/bin/python3 $startPath/$startProgram
    /usr/bin/python3 $startPath/$startProgram > $startPath/log/${startProgram%.*}.txt &
    ps -elf | grep $startProgram > $startPath/help/${startProgram%.*}.txt
    echo `ps -elf | grep $startProgram`
else
    echo "ERROR Cannot find $startPath/$startProgram"
fi

startPath=/home/pi/git/tablet/lightBarXXX
startProgram="lightBar.py"

found=`ls $startPath/$startProgram`

if [ $? == "0" ]; then
    echo starting /usr/bin/python3 $startPath/$startProgram
    /usr/bin/python3 $startPath/$startProgram > $startPath/log/${startProgram%.*}.txt &
    ps -elf | grep $startProgram > $startPath/help/${startProgram%.*}.txt
    echo `ps -elf | grep $startProgram`
else
    echo "ERROR Cannot find $startPath/$startProgram"
fi