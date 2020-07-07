#Author: Todd Hayes
#intended for use at Active Climbing Augusta

import RPi.GPIO as GPIO
import time


#use pin numbers [1,40] = GPIO are 7,11,12,13,15,16,18,19,21,22,23,24,26,29,31,32,33,35-38,40.
GPIO.setmode(GPIO.BOARD)

f = open("Count.txt","w")
f.write("0")
f.close()

#Pin definitions, all used are on outermost side
#divide pin by 2 to find pin, with 1 (pin 2) being by power/activity lights
#single door trigger and echo pins for sensors 1 and 2

single1T = 12
single1E = 16

single2T = 18
single2E = 22

#double door trigger and echo pins for long distance sensors 1 and 2
double1T = 32
double1E = 36

double2T = 38
double2E = 40

#testing light for every time a measurement is taken
green = 7
GPIO.setup(green, GPIO.OUT)

#pin setup
GPIO.setup(single1T, GPIO.OUT)
GPIO.setup(single2T, GPIO.OUT)
GPIO.setup(single1E, GPIO.IN)
GPIO.setup(single2E, GPIO.IN)

GPIO.setup(double1T, GPIO.OUT)
GPIO.setup(double2T, GPIO.OUT)
GPIO.setup(double1E, GPIO.IN)
GPIO.setup(double2E, GPIO.IN)

#sensor setup
print ("Initializing startup")
GPIO.output(green, True)
GPIO.output(single1T,False)
GPIO.output(single2T,False)
GPIO.output(double1T,False)
GPIO.output(double2T,False)
GPIO.output(green, False)
time.sleep(2)

#measuring block for short range sensors/ single door
def measureDistance(TRIG, ECHO):
    
    #emit pulse
    GPIO.output(TRIG,True)
    time.sleep(0.00001) #pulse needs to be 1 micro second long
    GPIO.output(TRIG,False)
    #listen for echo
    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        end = time.time()
    duration = end - start
    #blink green light after sensor measurement
    GPIO.output(green, True)
    time.sleep(0.125)
    GPIO.output(green,False)
    #return distance in centimeters
    return (duration * 17150)

#this will only return 1 or 0, 1 if someone entered, 0 if not
#this behavior is bc this will be measuring a door that is entrance only
def singleDoor():
    #measure both sensors
    dist1 = measureDistance(single1T,single1E)
    dist2 = measureDistance(single2T,single2E)
    #if both measure the center of the door or less, there is someone in the doorway
    #half ~= 20 in ~= 50 cm
    if (dist1 < 50 and dist2 < 50):
        return 1
    else:
        return 0
    
#this will only return -1 or 0, -1 if someone left, 0 if not
#this behavior is bc this will be measuring a door that is exit only
def doubleDoor():
    #measure both sensors
    dist1 = measureDistance(double1T,double1E)
    dist2 = measureDistance(double2T,double2E)
    #if both measure the center of the door or less, there is someone in the doorway
    #half ~~~ 64 in ~= 162 cm
    if (dist1 < 162 and dist2 < 162 ):
        return -1
    else:
        return 0
    
#main loop
try:
    while (True):
        f = open("Count.txt","r")
        oldCount = int(f.read())
        f.close()
        time.sleep(.001)
        f = open("Count.txt","w")
        print ("measuring")
        """
        single = str(singleDoor())
        print ("single door: " + single)
        double = str(doubleDoor())
        print ("Double door: " + double)
        f.write(str(oldCount + int(single) + int(double)))
        """
        f.write(str(oldCount + 1))
        f.close()
        print ("Count updated")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    pass