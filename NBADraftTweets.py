# -*- coding: utf-8 -*-
"""
Created on Sun Jul 05 02:42:58 2015
Last updated: 9/29/17

This script uses Twitter api to collect tweets from the 2015 NBA draft
and store them in a sqlite3 database. Once all the tweets are stored
in the sqlite3 database, they are then output into a csv file which can 
be opened and read.

The purpose of this script was to teach myself to use the twitter api 
with python and to teach myself basic SQL commands

For privacy and security this script has been modified so that it does 
not include my Twitter app authentication information (CONSUMER_KEY, 
CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) has been removed.
Without it this script cannot run, and is useful for viewing the code only.

This script was originally created in 2015 and updated in 2017 for more 
clarity with comments.

@author: Soorya Kumar
"""

import twitter
import sqlite3 
import csv
import re

CONSUMER_KEY = 'XXXX'
CONSUMER_SECRET = 'XXXX'
OAUTH_TOKEN = 'XXXX'
OAUTH_TOKEN_SECRET = 'XXXX'
        

#for twitter package
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(domain='api.twitter.com', 
                              api_version='1.1',
                              auth=auth)

#number of tweets to collect
count = 100 

#screen name for a famous NBA reporter
screen_name = 'WojYahooNBA'

#screen name for an account I made that follows several people who tweet often about the NBA
#screen_name = 'NBADraft'

#connect to database and set up cursor
conn = sqlite3.connect('NBADraftReferenceTweets.sqlite3') 
cur = conn.cursor() 

#delete and create a temporary table that will be used to remove repititve tweets collected
cur.execute('DROP TABLE IF EXISTS Temp')
cur.execute('CREATE TABLE Temp (tweet TEXT, date INTEGER, username TEXT, twitter_handle TEXT, time_id INTEGER )')

#check if table in database already exists, if not create it, and query for tweets
tablename='F'
cur.execute('DROP TABLE IF EXISTS %s' %tablename)
cur.execute('CREATE TABLE %s (tweet TEXT, date INTEGER, username TEXT, twitter_handle TEXT, time_id INTEGER )' %tablename)

    
#collect tweets between a given time period (the beginning and end of the 2015 NBA draft)
statuses = twitter_api.statuses.user_timeline(screen_name=screen_name, count=count, since_id=614214365684854784, max_id=614286165559103488)    
    
#for each tweet collected store the text, date, username, twitter handle, and time_id into the database    
for i in range(len(statuses)):    
    cur.execute('INSERT INTO %s (tweet, date, username, twitter_handle, time_id) VALUES ( ?, ?, ?, ?, ?)' %tablename, (statuses[i]['text'], statuses[i]['created_at'], statuses[i]['user']['name'], statuses[i]['user']['screen_name'], statuses[i]['id']) ) 
conn.commit() 
    
#use the temporary table to delete repetitive tweets by transferring only distinct tweets to the temporary table
#deleting all tweets in the original table and tranferring the now unique tweets back to the original table
cur.execute('INSERT INTO Temp SELECT DISTINCT * FROM %s' %tablename)  
cur.execute('DELETE FROM %s' %tablename)
cur.execute('INSERT INTO %s SELECT * FROM Temp' %tablename)

#finished making changes to database
conn.commit() 

#get ready to print information to output
tweets=[]
print 'Tweets:' 

#select only the tweets and order tweets by time id
cur.execute('SELECT tweet FROM %s ORDER BY time_id' %tablename) 
#print information to standard output
for row in cur:    
    print row 
    tweets.extend(row)    

#open output file    
#ofile = open('WojDraft.csv',"w")
ofile = open('NBADraft_tweets.csv',"w")

#configure CSV
writer = csv.writer(ofile, delimiter='\t')

#select the time id, the tweets, and the dates and order tweets by time id
cur.execute('SELECT time_id, tweet, date FROM %s ORDER BY time_id' %tablename)

#print information to output csv file
for row in cur:    
    try:
        writer.writerow(row)
    except UnicodeEncodeError:
        text = re.findall('^(.+)\http:', row[1])
        rownew=[row[0],text,row[2]]
        
ofile.close    

cur.close()