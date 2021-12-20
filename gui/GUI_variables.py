import numpy as np
from tkinter.colorchooser import askcolor

from tkinter import W, Frame, LabelFrame, N, W, BooleanVar, StringVar, IntVar
from tkinter import ttk as tk


class IntVarSafe(IntVar):
    """Variant of IntVar which never throws errors, but silently sets itself to zero"""

    def get(self):
        try:
            return super().get()
        except:
            return 0


class GUI_variables:
    # General tab variables
    root = None
    mode = 'off'
    color_generator_name = "Static"
    console_output = None
    num_leds = 300
    audio_device = None
    color = np.array([255, 0, 0])
    color_hex = "#ff0000"
    hue = 0
    speed = 10
    speaker1 = speaker2 = 0
    brightness = 40
    ip = [192, 168, 1, 213]

    # screen tab variables
    screen_mode = None
    fullscreen = None
    capture_width = None
    capture_height = None
    capture_x_offset = None
    capture_y_offset = None

    def __init__(self, list_available_audio_devices_function):
        self.list_available_audio_devices = list_available_audio_devices_function

    def choose_color(self, button):
        color_tuple = askcolor(title="Choose color")
        self.color = np.array(color_tuple[0])
        self.color_hex = color_tuple[1]
        self.hue = rgb2hsv(self.color[0], self.color[1], self.color[2])[0]
        button['bg'] = self.color_hex

    def print_console(self, message: str):
        self.console_output.set(message)

    def setMode(self, rgb_effects, mode: str):
        self.mode = mode
        rgb_effects.display_mode(mode)

    def setNumLeds(self, num: int):
        self.num_leds = num

    def setSpeaker1(self, position: int):
        self.speaker1 = position

    def setSpeaker2(self, position: int):
        self.speaker2 = position

    def setBrightness(self, position: int):
        self.speaker1 = position

    def setSpeed(self, speed: int):
        self.speed = speed

    def setAudioDeviceFromIndex(self, audio_index:str):
        self.audio_device = self.list_available_audio_devices[audio_index]

