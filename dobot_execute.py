#input values max(3x3)
#example input

#[[1,1,1][0,0,0][2,2,2]]
#0 - red
#1 - green
#2 - blue

#block placement
#222
#000
#111

import RPi.GPIO as GPIO 
import time
from serial.tools import list_ports
from dobot_extensions import Dobot 

available_ports = list_ports.comports()
port = available_ports[0].device 
device = Dobot(port=port, verbose=True)
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

ir = 17 

GPIO.setup(ir, GPIO.IN)


for i in range(150):
	if not GPIO.input(ir):
		device.conveyor_belt_distance(0, False)
	else: 
		device.conveyor_belt_distance(50, True)
	time.sleep(0.05)

device.close()

