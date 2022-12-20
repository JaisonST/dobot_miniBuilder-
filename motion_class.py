from dobot_extensions import Dobot 
from serial.tools import list_ports
from time import sleep

class Motion():
    UNIT_VAL = 25

    def __init__(self):
        available_ports = list_ports.comports()
        print(f'available ports: {[x.device for x in available_ports]}')
        port = available_ports[0].device

        self.device = Dobot(port=port, verbose=True)
        (self.home_x, self.home_y, self.home_z, self.home_r, j1, j2, j3, j4) = self.device.pose()
        self.current_pos = {"x":0, "y": 0, "z":4}
    

    def go_home(self): 
        self.device.move_to(self.home_x, self.home_y, self.home_z, self.home_r, wait=True)

    def collect_block(self): 
        self.device.move_to(self.home_x, self.home_y, self.home_z - self.UNIT_VAL, self.home_r, wait = True)
        self.device.suck(True)
        self.go_home()
        sleep(2)
        self.device.suck(False)
    
    def disconnect(self):
        self.device.close()
    
