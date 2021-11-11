
# the sacn module must be the one modified by me
import my_sacn
from typing import List
import numpy as np
from math import ceil

class E131Module:
    num_universes = 0
    led_number = 0
    ip = None

    def __init__(self, led_number:int):
        # instructions at https://github.com/Hundemeier/sacn
        """Attention: the sacn module was modified by me! (inserted RGBfunction)"""
        self.sender = my_sacn.sACNsender()
        self.sender.start()
        self.set_led_number(led_number)

    def send_data(self, data: np.ndarray):
        start_index = 0
        for u in range(1, self.num_universes):
            self.sender[u].dmx_data = data[start_index:start_index + 510]
            start_index += 510
        self.sender[self.num_universes].dmx_data = data[start_index:]

    def close(self):
        self.sender.stop()

    def set_rgb_function(self, rgb_function):
        self.sender.set_RGBfunction(rgb_function)

    def set_led_number(self, led_number: int):
        self.led_number = led_number

        # deactivate all active universes
        for i in self.sender.get_active_outputs():
            self.sender[i].dmx_data = tuple([0]*512)    # set all leds to black to avoid visual glitches
            self.sender.deactivate_output(i)

        # calculate and activate necessary active universes
        self.num_universes = ceil((led_number*3)/510)
        for i in range(1, self.num_universes + 1):
            self.sender.activate_output(i)

            # configure universes
            self.sender[i].multicast = True
            self.sender[i].destination = self.ip

    def set_ip(self, ip: str):
        self.ip = ip
        for i in self.sender.get_active_outputs():
            self.sender[i].destination = self.ip
