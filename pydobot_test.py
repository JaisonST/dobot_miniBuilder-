from serial.tools import list_ports
from dobot_extensions import Dobot
import time


available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[3].device

device = Dobot(port=port, verbose=True)


(x, y, z, r, j1, j2, j3, j4) = device.pose()
print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

device.move_to(x + 20, y, z, r, wait=False)
device.move_to(x, y, z, r, wait=True)  # we wait until this movement is done before continuing

#device.conveyor_belt(1)
for i in range(0,5):
    device.conveyor_belt_distance(50, True)
    time.sleep(1)
device.conveyor_belt_distance(50, False)


device.close()