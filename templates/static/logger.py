import csv 
import smbus 
import time 
import os
import datetime

DEVICE     = 0x5C #device address
bus = smbus.SMBus(2)  # Rev 2 Pi uses 1

def read():
    
	
    with open("output.csv",'a') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        addr=DEVICE
        bus = smbus.SMBus(2)  # Rev 2 Pi uses 1
        data = bus.read_i2c_block_data(addr,0x00, 5)
        GetDateTime = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M")]
        temp = [str(data[2]) + "." + str(data[3])   +"C"+"  "]
        hum =  [str(data[0]) + "." + str(data[1]) + " %"+"  "]
        ora = GetDateTime
        datas =temp + hum + ora
        #print "Humidity = " + str(data[0]) + "." + str(data[1]) + "%"
        #print "Temperature : " + str(data[2]) + "." + str(data[3]) + "C"
        wr.writerow(datas)
        print "OK"
while True:
	read()
	time.sleep(1800)
