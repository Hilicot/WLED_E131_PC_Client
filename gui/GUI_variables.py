import numpy as np


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

    def __init__(self, rgb_effects):
        self.rgb_effects = rgb_effects

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

    def setColorGenerator(self, generator_name: str = "Static"):
        self.color_generator_name = generator_name
        self.rgb_effects.update_color_generator()

    def setAudioDeviceFromIndex(self, audio_index: str):
        self.audio_device = self.rgb_effects.list_available_audio_devices[audio_index]
