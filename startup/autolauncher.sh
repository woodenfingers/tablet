#!/bin/bash

# Edit /ect/rc_local
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
    echo starting $startPath/$startProgram
    /usr/bin/python3 $startPath/$startProgram > $startPath/log/${startProgram%.*}.txt &
    ps -elf | grep $startProgram > $startPath/help/${startProgram%.*}.txt
    echo `ps -elf | grep $startProgram`
else
    echo "ERROR Cannot find $startPath/$startProgram"
fi

