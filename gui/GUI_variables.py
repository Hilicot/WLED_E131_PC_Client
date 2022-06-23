import numpy as np
from screeninfo import get_monitors

class GUI_variables:
    # General tab variables
    root = None
    mode = 'rainbow'
    color_generator_name = "Rainbow"
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

    def __init__(self, rgb_effects):
        self.rgb_effects = rgb_effects
        self.svars = ScreenVariables()

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

    def setBrightness(self, brightness: int):
        self.brightness = brightness

    def setSpeed(self, speed: int):
        self.speed = speed

    def setColorGenerator(self, generator_name: str = "Static"):
        self.color_generator_name = generator_name
        self.rgb_effects.update_color_generator()

    def setAudioDeviceFromIndex(self, audio_index: str):
        self.audio_device = self.rgb_effects.get_audio_device_list()[0][audio_index]


class ScreenVariables:
    screen_mode = 'Average'
    saturation_boost = 100
    fullscreen = False
    screen = get_monitors()[0]
    capture_width = int(screen.width/2)
    capture_height = int(screen.height/2)
    capture_x_offset = int(screen.width/4)
    capture_y_offset = int(screen.height/4)

    def setScreenMode(self, mode: str):
        self.screen_mode = mode

    def setFullScreen(self, fullscreen: bool):
        self.fullscreen = fullscreen

    def setSaturationBoost(self, saturation_boost: int):
        self.saturation_boost = saturation_boost

    def setWidth(self, width: int):
        self.capture_width = width

    def setHeight(self, height: int):
        self.capture_height = height

    def setXOffset(self, offset: int):
        self.capture_x_offset = offset

    def setyOffset(self, offset: int):
        self.capture_y_offset = offset
