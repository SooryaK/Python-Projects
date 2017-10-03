#!/usr/bin/env python

#This script is written for a Raspberry Pi.
#The purpose of this script is to make use of the Raspberry Pi's GPIO pins
#to turn on a lamp that is connect to a relay switch, that is connected to 
#GPIO pin 24 of the raspberry pi, to help me wake up in the morning.
#
#Additionaly another GPIO pin, pin 25, is hooked up to a button to recieve
#input. The lamp that was turned on will stay on until the button hooked up
#to pin 25 is pressed. Then the lamp stays on for 30 more minutes (to make
#sure I can't fall back asleep) before turning off.
#
#The raspberry Pi is positioned so that I have to get out of bed to press
#the button and turn the light off.
#
#This script is run by cron jobs on the Raspberry Pi at a time my wake up time,
#which I set.
#
#Created by: Soorya Kumar

import RPi.GPIO as GPIO
import time
import datetime
import csv

#setup GPIO pin 24 for output of 5V to send to the relay switch
#set GPIO pin 25 to recieve input
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

#set GPIO pin 24 to high to send 5V to the relay switch and turn the lamp on
#record the time the light was turned on
GPIO.output(24, GPIO.HIGH)
timeStart = datetime.datetime.now()

#a button is wired between the 3v3 pin and GPIO pin 25
#while the button is not pressed GPIO pin 25 detects no output
#when the button is first pressed down the circuit is complete and
#pin 25 recieves a signal (or in otherwords there is a rising edge of output)
#when the button is then released (completing a regular button press), the circuit
#is disconnected again and pin 25 no longer recieves a voltage signal 
#(a falling edge occurs). Once a rising and falling edge are observed by pin 25
#it is known that the button press is complete
#
#the time the button is pressed is recorded
GPIO.wait_for_edge(25, GPIO.RISING)
GPIO.wait_for_edge(25, GPIO.FALLING)
timePressed = datetime.datetime.now()

#the time between when the lamp was turned on and
#when the button was pressed is recorded and converted to seconds
#and printed to standard output
timeToPress=timePressed-timeStart
timeToPressSeconds=timeToPress.total_seconds()
print timeToPressSeconds

#format the current date into string
fmt ='%Y-%m-%d %H:%M:%S' 
d = datetime.datetime.now()
d_string = d.strftime(fmt)

#write the date and how long it took for me to get out of bed 
#and press the button to a csv file, to keep track of how long
#it takes me to get out of bed each day 
ofile = open('/home/sooryak/getoutofbedtimes.csv',"a")
writer = csv.writer(ofile, delimiter=',')
writer.writerow([d_string,timeToPressSeconds])

#keep lamp on for 30 min (after the button press is complete)
time.sleep(1800)

#turn off lamp and end the program
GPIO.output(24, GPIO.LOW)
quit()