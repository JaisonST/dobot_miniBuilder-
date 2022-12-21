from dobot_extensions import Dobot 
from serial.tools import list_ports
from time import sleep
import pygame 
import pygame.camera

import RPi.GPIO as GPIO 

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

ir = 17
GPIO.setup(ir, GPIO.IN)

class Motion():
    UNIT_VAL = 25

    def get_ir(self):
        return not GPIO.input(ir)
 
    def get_color(self):
        pygame.init()
        pygame.camera.init()
        cam = pygame.camera.Camera('/dev/video0', (640, 480))
        cam.start()
        img = cam.get_image()
        [r, g, b, a] = img.get_at((320, 240))
        vals = [r,g,b]
        index = vals.index(max(vals))
        cam.stop()
        return index

    def __init__(self):
        available_ports = list_ports.comports()
        print(f'available ports: {[x.device for x in available_ports]}')
        port = available_ports[0].device

        self.device = Dobot(port=port, verbose=True)
        (self.home_x, self.home_y, self.home_z, self.home_r, j1, j2, j3, j4) = self.device.pose()
        self.current_pos = {"x":0, "y": 0, "z":4}
        self.stacks = [0,0,0]
        self.place_index = [0,0,0] 
    

    def go_home(self): 
        self.device.move_to(self.home_x, self.home_y, self.home_z, self.home_r, wait=True)

    def collect_block(self):
        self.device.conveyor_belt_distance(25, True)
        while not self.get_ir():
            sleep(0.025)
        self.device.conveyor_belt_distance(0, False)
    
        self.device.move_to(self.home_x, self.home_y, self.home_z - self.UNIT_VAL, self.home_r, wait = False)
        self.device.suck(True)
        self.go_home()
        self.device.move_to(self.home_x, self.home_y, self.home_z + 25, self.home_r, wait = False)

        self.device.move_to(self.home_x - 45, self.home_y + 60, self.home_z + 25, self.home_r, wait = False)
        self.device.move_to(self.home_x - 45, self.home_y + 60, self.home_z - 10, self.home_r, wait = False)
        sleep(3)
        color = self.get_color()
        sleep(1)
        self.device.move_to(self.home_x - 45, self.home_y + 60, self.home_z + 25, self.home_r, wait = False)
        self.go_home()
        return(color)

    def stack(self, color):
        self.device.move_to(self.home_x, self.home_y, self.home_z + self.UNIT_VAL, self.home_r, wait = True)
        
        self.device.move_to(self.home_x, self.home_y - (4 * self.UNIT_VAL + 2*((color) * self.UNIT_VAL)), self.home_z + self.UNIT_VAL, self.home_r, wait = True)
        self.device.move_to(self.home_x, self.home_y - (4 * self.UNIT_VAL + 2*((color) * self.UNIT_VAL)), self.home_z - (self.UNIT_VAL * (3 - self.stacks[color])), self.home_r, wait = True)
        self.device.suck(False)       
        self.stacks[color] += 1 
        self.device.move_to(self.home_x, self.home_y - (4 * self.UNIT_VAL + 2*((color) * self.UNIT_VAL)), self.home_z + self.UNIT_VAL, self.home_r, wait = True)
        self.go_home()

    def unstack(self, color):
        if self.stacks[color] == 0 :
            print("ERROR : NO STACK OF THE COLOR")
            return
        self.device.move_to(self.home_x, self.home_y, self.home_z + self.UNIT_VAL, self.home_r, wait = True)
        self.device.move_to(self.home_x, self.home_y - (4 * self.UNIT_VAL + 2*((color) * self.UNIT_VAL)), self.home_z + self.UNIT_VAL, self.home_r, wait = True)
        self.stacks[color] -= 1 
        self.device.move_to(self.home_x, self.home_y - (4 * self.UNIT_VAL + 2*((color) * self.UNIT_VAL)), self.home_z - (self.UNIT_VAL * (3 - self.stacks[color])), self.home_r, wait = True)
        self.device.suck(True)
        self.device.move_to(self.home_x, self.home_y - (4 * self.UNIT_VAL + 2*((color) * self.UNIT_VAL)), self.home_z + self.UNIT_VAL, self.home_r, wait = True)
        self.go_home()
        
    def place(self, index):
        new_y = self.home_y + (5 * self.UNIT_VAL) 
        self.device.move_to(self.home_x, self.home_y, self.home_z + self.UNIT_VAL, self.home_r, wait = False)
        self.device.move_to(self.home_x - (1 * self.UNIT_VAL), self.home_y - (8 * self.UNIT_VAL), self.home_z + self.UNIT_VAL, self.home_r, wait = False)
        self.device.move_to(self.home_x - (6 * self.UNIT_VAL), self.home_y - (8 * self.UNIT_VAL), self.home_z + self.UNIT_VAL, self.home_r, wait = False)
        self.device.move_to(self.home_x - (6 * self.UNIT_VAL), self.home_y - (10 * self.UNIT_VAL), self.home_z + self.UNIT_VAL, self.home_r, wait = False)

        self.device.move_to(self.home_x - (6 * self.UNIT_VAL + 1.1*((index) * self.UNIT_VAL)), self.home_y - (10 * self.UNIT_VAL), self.home_z + self.UNIT_VAL, self.home_r, wait = False)
        self.device.move_to(self.home_x - (6 * self.UNIT_VAL + 1.1*((index) * self.UNIT_VAL)), self.home_y - (10 * self.UNIT_VAL), self.home_z - (self.UNIT_VAL * (3 - self.place_index[index])), self.home_r, wait = False)
        self.device.suck(False)

        self.device.move_to(self.home_x - (6 * self.UNIT_VAL + 1.1*((index) * self.UNIT_VAL)), self.home_y - (10 * self.UNIT_VAL), self.home_z + self.UNIT_VAL, self.home_r, wait = False)

        self.place_index[index]+=1

        self.device.move_to(self.home_x - (6 * self.UNIT_VAL), self.home_y - (10 * self.UNIT_VAL), self.home_z + self.UNIT_VAL, self.home_r, wait = False)
        self.go_home()

    def get_location(self):
        print(self.device.pose())

    def has_stack(self, color):
        if color > 2 :
            return False
        if self.stacks[color] == 0:
            return False
        return True 
        
    def disconnect(self):
        self.device.close()
    




