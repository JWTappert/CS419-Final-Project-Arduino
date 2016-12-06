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
                     passwd='Rubean1',
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

    # Set timer for 120 seconds on this function with parameter passed
    threading.Timer(120.0, check_readings).start()

    # Get last 5 entries from node0 and node1
    cur.execute("SELECT temp FROM readings WHERE node_id=%s ORDER BY time DESC LIMIT 5", (str(0)))
    node0 = cur.fetchall()

    cur.execute("SELECT temp FROM readings WHERE node_id=%s ORDER BY time DESC LIMIT 5", (str(1)))
    node1 = cur.fetchall()

    avgTemp0 = 0.0
    avgTemp1 = 0.0

    # Average them
    for n in xrange(0, cur.rowcount):
        avgTemp0 += node0[n][0]
        avgTemp1 += node1[n][0]

    avgTemp0 = avgTemp0/cur.rowcount
    avgTemp1 = avgTemp1/cur.rowcount

    res = avgTemp0 - avgTemp1

    # if node0 - node1 > 2 then send_email(True)
    # if node0 - node1 < -2 then send_email(False)
    if res > 2:
        send_email(True)
    elif res < -2:
        send_email(False)

check_readings()
