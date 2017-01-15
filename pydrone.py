'''
Interface with the Ar Drone

MIT License

Copyright (c) 2016 Jacob Laney

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import socket
import struct

IP_ADDR = "192.168.1.1"
PORT = 5556
HOST = (IP_ADDR, PORT)

class DroneController:
    def __init__(self):
        self.isFlying = False
        self.sequence = 0 # counter attached to each message
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.reset()
        return

    def liftoff(self):
        self.isFlying = True
        self.sequence += 1  # send trim command
        self.connection.sendto("AT*FTRIM=" + str(self.sequence) + "\r", HOST)
        cmd = 0x11540200    # send liftoff command
        self.send("AT*REF=", cmd)
        return

    def land(self):
        self.isFlying = False
        cmd = 0x11540000
        self.send("AT*REF=", cmd)
        return

    def kill(self):
        cmd = 0x11540100
        self.send("AT*REF=", cmd)
        return

    def hover(self):
        self.reset();
        cmd = "0,0,0,0,0"
        self.send("AT*PCMD=", cmd)
        return

    def move(self):
        moveBit = 1
        cmd = "1,"
        cmd += str(self.left_right_tilt) + ","
        cmd += str(self.front_back_tilt) + ","
        cmd += str(self.vertical_speed) + ","
        cmd += str(self.angular_speed)
        self.send("AT*PCMD=", cmd)
        return

    def send(self, tag, command):
        self.sequence += 1
        message = tag + str(self.sequence) + "," + str(command) + "\r"
        self.connection.sendto(message, HOST)
        return

    def reset(self):
        self.vertSpeed = 10
        self.latSpeed = 10
        self.angSpeed = 5
        self.left_right_tilt = 0; # movement fields
        self.front_back_tilt = 0;
        self.vertical_speed = 0;
        self.angular_speed = 0;
        return

    def float_to_int(self, value):
        x = ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', value))
        return int(x, 2)

    def set_left_right(self, value):
        self.left_right_tilt = self.float_to_int(value * self.latSpeed)
        return;

    def set_front_back(self, value):
        self.front_back_tilt = self.float_to_int(value * self.latSpeed)
        return

    def set_angular_speed(self, value):
        self.angular_speed = self.float_to_int(value * self.angSpeed)
        return

    def set_vertical_speed(self, value):
        self.vertical_speed = self.float_to_int(value * self.vertSpeed)
        return
