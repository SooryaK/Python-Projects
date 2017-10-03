#!/usr/bin/env python
#
#This script is written for a Raspberry Pi.
#
#The purpose of this script is to send a txt file of my workouts
#(which I manually type into the txt file) to some of my friends
#for accountability (to motivate me to workout, because if I don't
#my friends will see).
#
#This script is run by cron jobs on the Raspberry Pi once a week 
#at a time which I set.
#
#For privacy and security, My account id and authentication token for
#twilio are not provided. The phone number provided to me from twilio,
#as well as the phone numbers of my friends are similarly not provided.
#Without it this script cannot run, and is useful for viewing the code only.
#
#Created by: Soorya Kumar

import datetime
from twilio.rest import TwilioRestClient

#twilio account info
account_sid = "XXXX"
auth_token = "XXXX"

#format current date into string
#and get the dates of the current week
fmt = '%m/%d/%Y'
d = datetime.datetime.now()
d_now_string = d.strftime(fmt)
d_weekago = datetime.datetime.now() - datetime.timedelta(6)
d_weekago_string = d_weekago.strftime(fmt)

#create the title of the week, which changes based on the day
#the script is executed
#For Example
#"Soorya's Workouts for 04/03/2017 - 04/09/2017" would be the title if the
#code was executed on 04/09/2017
title = "Soorya's Workouts for " + d_weekago_string + " - " + d_now_string

#using Twilio's api
client = TwilioRestClient(account_sid, auth_token)

#open the txt file where I have manually typed in my workouts
#for the week
workouts_file = open('/home/pi/workouts.txt', 'r')

#combine the title with the workouts
workouts = title + workouts_file.read()

#create the message to be sent to one of my friends
#YYYYYYYYYY is the number Twilio has given me to send texts from
#ZZZZZZZZZZ is the number of my friend
message1 = client.messages.create(body=workouts,
    to="+YYYYYYYYYY",
    from="+ZZZZZZZZZZ")

#create the message to be sent to another one of my friends
#YYYYYYYYYY is the number Twilio has given me to send texts from
#AAAAAAAAAA is the number of my friend    
message2 = client.messages.create(body=workouts,
    to="+YYYYYYYYYY",
    from="+AAAAAAAAAA")

#send the texts to my friends
print(message1.sid)
print(message2.sid)

#write the workouts to my own txt files so I can keep
#a history of them
cumulative_file = open('/home/pi/cumulative_workouts.txt', 'a')
cumulative_file.write(workouts+"\n")