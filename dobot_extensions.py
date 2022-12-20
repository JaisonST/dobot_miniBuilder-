import pydobot
import math
import struct
from pydobot.message import Message 
from ctypes import *

class EMotor(Structure):
    _pack_ = 1
    _fields_ = [
        ("index", c_byte), 
        ("isEnabled", c_byte), 
        ("speed", c_int32)
    ]


class Dobot(pydobot.Dobot):
    

    @staticmethod
    def _extract_cmd_index(response):
        return struct.unpack_from('I', response.params, 0)[0]

    def _set_stepper_motor_distance(self, speed, isEnabled=True):
        msg = Message()
        msg.id = 135
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray([0x01]))

        motorOn = 0 
        f_speed = 0 
        if isEnabled: 
            motorOn = 1 
            f_speed = speed
        else: 
            motorOn = 0 
        emotor = EMotor()
        emotor.index = 2 
        emotor.isEnabled = motorOn
        emotor.speed = f_speed

        
    
        msg.params.extend(bytearray(emotor))
        
        return self._send_command(msg)

    def conveyor_belt_distance(self, speed, isEnabled):
        if speed> 100:
            raise pydobot.dobot.DobotException("Speed must be <= 100 mm/s")

        return self._extract_cmd_index(self._set_stepper_motor_distance(int(speed), isEnabled))