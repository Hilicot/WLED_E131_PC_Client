import colorsys
import numpy as np


class Mode_info:
    def __init__(self, name: str, label: str = 'undefined', RGBfunction: callable = lambda: None,
                 setup_function: callable = lambda: None, close_function: callable = lambda: None):
        self.name = name
        self.label = label
        self.RGBfunction = RGBfunction
        self.setup_function = setup_function
        self.close_function = close_function


def hsv2rgb(h, s, v):
    return np.round_(np.array(colorsys.hsv_to_rgb(h/255, s/255, v/255))*255)


def rgb2hsv(r, g, b):
    return np.round_(np.array(colorsys.rgb_to_hsv(r/255, g/255, b/255))*255)

def np_hsv2rgb(hsv):
    [h,s,v] = hsv / 255
    return np.array(np.round_(np.array(colorsys.hsv_to_rgb(h, s, v))*255))
