import RPi.GPIO as GPIO ##import the gpio lib
from time import sleep ##import time for delays

##setup streamer
from ISStreamer.Streamer import Streamer
streamer = Streamer(bucket_name="Double Button LED", bucket_key="LED TESTS", access_key="2S9z7XNGuNCCoC3uPcjyi8bbN4nEqqCH")

counter = 0


GPIO.setwarnings(False) ## disables gpio messages that they are in use
GPIO.setmode(GPIO.BOARD) ## which pin config to use

GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)

GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

state = 0

inc = 1

prev_input = 2

## make a function to log with streamer
def postLog():
  streamer.log("state", state)
  streamer.log("prev_input", prev_input)
  streamer.log("increment", inc)

try:
  while True:
    counter += 1
    if ( GPIO.input(16) == True ):
      if (inc == 1):
        state = state + 1;
      else:
        state = state - 1;
      
      if (state == 3):
        inc = 0
        prev_input = 1
        postLog()
      elif (state == 0):
        inc = 1
        prev_input = 2
        postLog()

      if (state == 1):
        GPIO.output(7, GPIO.LOW)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        prev_input = 2
        postLog()
      elif (state == 2):
        GPIO.output(7, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        prev_input = 2
        postLog()
      elif (state == 3):
        GPIO.output(7, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        postLog()
      else:
        GPIO.output(7, GPIO.HIGH)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        postLog()

      streamer.log("button_1", "pressed")
      sleep(0.2);

    ##when button 2 is pressed
    if(GPIO.input(18) == True):
      if( state == 1 or 2 and prev_input != 1):
        GPIO.output(7, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        prev_input = 1
        state = 3
        inc = 0
        postLog()
      elif (state == 0 and prev_input != 0):
        GPIO.output(7, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        prev_input = 1
        state = 3
        inc = 0
        postLog()
      elif (state == 3 and prev_input != 0):
        GPIO.output(7, GPIO.HIGH)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        prev_input = 0
        state = 0
        inc = 1
        postLog()

      streamer.log("button_2", "pressed")
      sleep(0.2);
except KeyboardInterrupt:  
  # here you put any code you want to run before the program   
  # exits when you press CTRL+C  
  print "\n", counter # print value of counter  

except:  
  # this catches ALL other exceptions including errors.  
  # You won't get any error messages for debugging  
  # so only use it once your code is working  
  print "Other error or exception occurred!"

finally:  
    GPIO.cleanup() # this ensures a clean exit  
    streamer.close()












