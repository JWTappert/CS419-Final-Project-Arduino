# !/usr/bin/python

import sys
import serial
import signal
import time
import MySQLdb

# Make sure usage is correct
if len(sys.argv) != 2:
    print "usage: ./baseStation.py /dev/tty.usbXXX"
    sys.exit(1)

# Grab command line arg
port = sys.argv[1]


# Register signal and define signal function
def signal_handler(signal, frame):
    print '\nExiting with the highest amount of grace'
    ser.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

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
    ser = serial.Serial(port, 9600)
    print "Serial port opened successfully."

    # Take a quick nap
    time.sleep(1)
except:
    print "Unable to open serial port, closing."
    sys.exit(1)

time.sleep(5)
ser.flushInput()
ser.flushOutput()
time.sleep(.1)
print "starting..."
ser.write("S")
print "waiting 60 seconds..."
time.sleep(60)
print "sending request for data..."
ser.write("R0")
print "request sent..."


while True:
    data = ser.read(5)
    print data
    q = "INSERT INTO readings (node_id, temp) VALUES ".format(0, data)
    cur.execute("INSERT INTO readings (node_id, temp) VALUES (%s, %s) ", (0, data))
    db.commit()
