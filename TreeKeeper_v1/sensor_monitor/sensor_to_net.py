import os
import socket
import json
import time
import time, sys, signal, atexit                                                                                                                              
#import pyupm_mma7660 as upmMMA7660

#air
import pyupm_gas as TP401

#flame
import pyupm_yg1006 as upmYG1006

#light
import pyupm_grove as grove

#moisture
import pyupm_grovemoisture as upmMoisture

#temperature
import pyupm_otp538u as upmOtp538u

#water
import pyupm_grovewater as upmGrovewater

HOST = "127.0.0.1"
PORT = 41234
INTERVAL = 60

#air   AIO1
airSensor = TP401.TP401(1)

# Instantiate a flame sensor on digital pin D3
myFlameSensor = upmYG1006.YG1006(3)

# Create the light sensor object using AIO pin 2
light = grove.GroveLight(2)

# Instantiate a Grove Moisture sensor on analog pin A3
myMoisture = upmMoisture.GroveMoisture(3)

# analog voltage, usually 3.3 or 5.0
OTP538U_AREF = 5.0 

# Instantiate a OTP538U on analog pins A0 and A1
# A0 is used for the Ambient Temperature and A1 is used for the
# Object temperature.
myTempIR = upmOtp538u.OTP538U(0, 1, OTP538U_AREF)

# Instantiate a Grove Water sensor on digital pin D2
myWaterSensor = upmGrovewater.GroveWater(2)


## Exit handlers ##
# This function stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
    raise SystemExit

# This function lets you run code on exit, including functions from myDigitalAccelerometer
def exitHandler():
    print "Exiting"
    sys.exit(0)

# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)

def collect_data():
    temperature_value = myTempIR.ambientTemperature()
    send_data("temp",temperature_value)

    air_value = airSensor.getSample()
    if(air_value < 50):
        air_value = 1
    elif(air_value >= 50 and air_value < 200):
        air_value = 2
    elif(air_value >= 200 and air_value <400):
        air_value = 3
    elif(air_value >= 400 and air_value <600):
        air_value = 4 
    else:
        air_value =5
    send_data("airquality",air_value)
    
    flame_value = myFlameSensor.flameDetected()
    if(flame_value):
        send_data("flame",1)
    else:
        send_data("flame",0)

    light_value = light.value()
    send_data("light",light_value)
    
    water_value = myWaterSensor.isWet()
    if(water_value):
        send_data("water", 1)
    else:
        send_data("water", 0)

    moisture_val = myMoisture.value()
    if (moisture_val >= 0 and moisture_val < 300):
        moisture_result = 1 
    elif (moisture_val >= 300 and moisture_val < 600):
        moisture_result = 2 
    else:
        moisture_result = 3
    send_data("moist",moisture_result)
    
    print "(%d,%d,%d,%d,%d,%d)" % (air_value,flame_value,light_value,moisture_result,temperature_value,water_value)

def send_data(name,value):
    msg = {
        "n": name,
        "v": value,
	'on': (int(time.time()) * 1000)
    }
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(msg), (HOST, PORT))


while(1):
    collect_data()
    time.sleep(10)
