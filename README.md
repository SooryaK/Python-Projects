# Python-Projects
Simple Python Projects I have done on my own. Some are Raspberry Pi projects.

wakeuplamp.py 
This script utilizes GPIO pins on the Raspberry Pi to turn on a lamp (which is connected to a relay, which itself is connected to the Raspberry Pi). The script is meant to be run by cron jobs so that it automatically runs at a specified time, to help me wake up in the mornings. The Raspberry Pi is also meant to be wired to a button. Once the script is run the lamp will not turn off until the button is pressed. After the button is pressed, the script waits 30 minutes before the lamp is turned off. The time it takes for me to press the button once the light goes off (the time it takes me to get out of bed) is also calculated and recorded.

workout-sms.py
This script utilizes the Twilio api to send a txt file as a text to phone numbers that are specified in the script. I can manually type the workouts that I have done during the course of a week into the txt file, and then this program will send my workouts to my friends. It's purpose is to motivate me to workout, using my friends as accountability, since I wouldn't want them to see I wasn't working out. The script is also meant to be run by cron jobs, once a week, in order to automatically deliver the workouts that I have manually typed into the txt file to my friends each week.

NBADraftTweets.py
This script utilizes the Twitter api to collect tweets from a Twitter account about the 2015 NBA Draft (I'm a basketball fan). After collecting the tweets, the script stores the tweets in an sqlite3 database, as well as in csv format. It's purpose was simmply to allow me to experiment with the Twitter api, sqlite3, and the basics of SQL.
