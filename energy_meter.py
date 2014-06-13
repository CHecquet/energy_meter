#!/usr/bin/python

#serial
import serial
#log
import string
import time
#graph
import numpy
import pylab as pl

serialDev='/dev/ttyUSB0'

ser = serial.Serial(serialDev, 57600, timeout=1)
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)

print 'record 1 value from ', serialDev
print 'format: date\tpower'
print 'example:'
line = "123.456"
val=float(line)
current_time = time.localtime()
strTime=time.strftime('%d/%m/%Y %H:%M:%S', current_time)
strData=strTime+",\t" +str(val)
print strData

print '\nshow serial information:\n'
#Plink version
ser.write("*VER");
line = ser.readline()
print("*VER=|"+line+"|")

#many information
ser.write("*F01");
line = ser.readline()
line = ser.readline()
print("*F01=|"+line+"|")

ser.write("*NAM");
line = ser.readline()
print("*NAM=|"+line+"|")
device_head=line

#plot data
data=numpy.empty(32)
data.fill(numpy.NAN)
i=data.size
##setup GUI window
pl.ion()
fig = pl.gcf()
fig.canvas.set_window_title('Power meter ('+'Gentec-Plink='+device_head+')')

#data recording
print '#date (date time),\tpower (W)'
#for i in range(0,3):
while(True):
  #ask and get data
  ser.write("*CVU");
  ##line = "123.456"
  line = ser.readline()
  line = ser.readline()
###  print("*CVU=|"+line+"|\n")
  #get time
  current_time = time.localtime()
  #convert to float
  val=float(line)
  #convert to string, i.e. line
  strTime=time.strftime('%d/%m/%Y %H:%M:%S', current_time)
  strData=strTime+",\t" +str(val)
  #show
  print strData
  #write to file
  f = open("log_GentecPlink.txt","a")
  f.write(strData);f.write("\n")
  f.close()
  #plot data
  ##check boundary
  if(i<0):
    i=1
  i-=1
  ##shift previous values
  for j in range(i+1,data.size-1):
#    print(j+1)
    data[j]=data[j+1]
  ##set current value
  data[data.size-1]=val
  ##layout
  pl.clf()
  pl.xlim([0,data.size])
  pl.xlabel('time (s)')
  pl.ylabel('power (W)')
  ##plot
  pl.plot(data)
  pl.draw()
  #wait a while
  time.sleep(0.1)


