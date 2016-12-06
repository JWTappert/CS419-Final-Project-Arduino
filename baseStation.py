# !/usr/bin/python

import threading
import smtplib
import sys
import serial
import signal
import time
import MySQLdb

from email.mime.text import MIMEText

# Make sure usage is correct
if len(sys.argv) != 2:
    print "usage: ./baseStation.py /dev/tty.usbXXX"
    sys.exit(1)

# Grab command line arg
port = sys.argv[1]


# Register signal and define signal function
def signal_handler(signal, frame):
    print '\nExiting with the highest amount of grace'

    # Make sure nodes stop collecting data
    ser.write("T")

    # Close serial port and exit
    ser.close()
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

'''
# Use all the SQL you like
cur.execute("SELECT * FROM readings")

# print all the first cell of all the rows
for row in cur.fetchall():
    print "{0} {1} {2} {3}".format(row[0], row[1], row[2], row[3])

db.close()

sys.exit(0)
'''

try:
    # Open up the serial port with a 2 second timeout
    ser = serial.Serial(port, 9600, timeout=2.0)
    print "Serial port opened successfully."

    # Take a quick nap
    time.sleep(1)
except:
    print "Unable to open serial port, closing."
    sys.exit(1)


'''
This function will execute once every 60 seconds.

As a parameter you need to pass what node it will be collecting data for.

If the data received is less than 5 characters that means a partial packet
was received or the timeout was reached and nothing was received.

In that case several more attempts will be made to collect the data.

Once all attempts have been made then the data will be passed along for storage
'''


def get_reading(node_id):

    # Set timer for 60 seconds on this function with parameter passed
    threading.Timer(interval=60, function=get_reading, args=[node_id]).start()

    # Flush out anything left in the serial buffer
    ser.flushInput()
    ser.flushOutput()

    # Variable to track number of attempts made so far
    nAttempts = 0

    # print "sending request for data...", node_id
    # Send broadcast stating what node needs to Tx
    ser.write(node_id)
    # print "request sent...", node_id
    # Read Tx from node
    data = ser.read(5)
    nAttempts += 1

    # Verify expected value was received, if not make 3 more attempts
    # Since this is being deployed in a home we can expect the temperature
    # to be in the double digits, and we are recording to the hundredth degree
    # plus the point makes 5 characters
    # If data isn't 5 characters then either partial data was received, no data
    # was received, or everyone in the house has left because it is too cold/hot
    while len(data) < 5 and nAttempts < 4:
        nAttempts += 1
        # print "shit got fucked"
        # print "sending ANOTHER request for data...", node_id
        ser.write("S")
        ser.write("0")
        # print "request sent...", node_id
        data = ser.read(5)

    # Send off the data for storage
    # print "Node: ", node_id, "data: ", data
    store_data(node_id, data)


# This function will add data to the db we are connected to
def store_data(node_id, temp):

    # If the data is still less than 5 here then after 4 attempts nothing was
    # received & data loss has occurred, store a dummy value that can be easily
    # ignore later
    if len(temp) < 5:
        cur.execute("INSERT INTO readings (node_id, temp) VALUES (%s, %s) ", (0, 666.0))
        db.commit()

    # Store data in connected db
    cur.execute("INSERT INTO readings (node_id, temp) VALUES (%s, %s) ", (node_id, temp))
    db.commit()

    # Flush out anything left in the serial buffer
    ser.flushInput()
    ser.flushOutput()


# Flush out serial buffers before starting, then broadcast Start to all nodes
ser.flushInput()
ser.flushOutput()
time.sleep(.1)
print "starting..."
ser.write("S")
time.sleep(5)  # Give the nodes some time to get things started

'''
Start timers for each node. In this case node 0 will be asked to Tx after 60s
and node 1 will be asked to Tx after 75s.

From that point forward each node will Tx data every 60s.
'''
get_reading("0")
time.sleep(15)
get_reading("1")
