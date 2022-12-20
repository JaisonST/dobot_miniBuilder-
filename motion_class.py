from dobot_extensions import Dobot 
from serial.tools import list_ports
from time import sleep
import pygame 
import pygame.camera 


class Motion():
    UNIT_VAL = 25

    def get_color(self):
        pygame.init()
        pygame.camera.init()
        cam = pygame.camera.Camera('/dev/video0', (640, 480))
        cam.start()
        img = cam.get_image()
        [r, g, b, a] = img.get_at((320, 240))
        vals = [r,g,b]
        index = vals.index(max(vals))
        return index

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
        self.device.move_to(self.home_x, self.home_y, self.home_z + 25, self.home_r, wait = True)

        self.device.move_to(self.home_x - 45, self.home_y + 60, self.home_z + 25, self.home_r, wait = True)
        self.device.move_to(self.home_x - 45, self.home_y + 60, self.home_z - 10, self.home_r, wait = True)
        color = self.get_color()
        sleep(2)
        self.device.move_to(self.home_x - 45, self.home_y + 60, self.home_z + 25, self.home_r, wait = True)
        self.go_home()
        sleep(2)
        print("HAAH THIZ ISM", color)
        self.device.suck(False)
        return(color)
    
    def disconnect(self):
        self.device.close()
    
