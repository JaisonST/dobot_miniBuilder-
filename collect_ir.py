import RPi.GPIO as GPIO 
import time
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

ir = 17

GPIO.setup(ir, GPIO.IN)

while True: 
	print(GPIO.input(ir))
	time.sleep(1)
