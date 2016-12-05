import threading
import smtplib
import sys
import signal
import time
import MySQLdb

from email.mime.text import MIMEText


# Make sure usage is correct
if len(sys.argv) != 2:
    print "usage: ./baseStation.py your@email.com"
    sys.exit(1)

# Grab command line arg
email = sys.argv[1]

print "Email: ", email

# Register signal and define signal function
def signal_handler(signal, frame):
    print '\nExiting with the highest amount of grace'
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# Establish connection to database
db = MySQLdb.connect(host='localhost',
                     user='root',
                     passwd='',
                     db='tempReadings')

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

def send_email(isCold):

    msg = ""

    # Create appropriate message
    if isCold:
        msg = "The room is too cold!"
    else:
        msg = "The room is too hot!"

    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)  # port 465 or 587
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, 'adamellienaeevey')
    server.sendmail(email, email, msg)
    server.close()

def check_readings():

    # Set timer for 60 seconds on this function with parameter passed
    threading.Timer(120.0, check_readings()).start()

    # http://stackoverflow.com/questions/1313120/retrieving-the-last-record-in-each-group
    # ^^possible solution?

    # Get last 5 entries from node0 and node1
    # Average them

    # if node0 - node1 > 2 then send_email(True)
    # if node0 - node1 < -2 then send_email(False)

send_email(False)
