import numpy as np

from utils import *
from typing import Dict, List
from E131Module import E131Module
import audio_functions
from screen_fuctions import screen_average
from gui.GUI_variables import GUI_variables
import scipy.interpolate


class RGBEffects:
    led_num = 300
    audio_stream = None
    audio_rate = 0
    portaudio = None
    hue_shift = 0
    color_generator = lambda x: None
    past_states = None
    get_audio_device_list = audio_functions.list_available_audio_devices

    # TODO audio_spectrum
    def __init__(self):
        self.mode_list = {'off': Mode_info('off', 'off', lambda: None, setup_function=self.clear_leds),
                          "rainbow": Mode_info('rainbow', "Rainbow", self.rainbow),
                          "screen_mirroring": Mode_info("screen_mirroring", 'Screen Mirroring', self.screen_mirroring),
                          "audio_static": Mode_info("audio_static", 'Audio Visualizer (Static)',
                                                    self.audio_static, self.setup_audio_stream,
                                                    self.close_audio_stream),
                          "audio_speakers": Mode_info("audio_speakers", 'Audio Visualizer (Speakers)',
                                                      self.audio_speakers, self.setup_audio_stream,
                                                      self.close_audio_stream),
                          "audio_spectrum": Mode_info("audio_spectrum", 'Audio Visualizer (Spectrum)',
                                                      self.audio_spectrum, self.setup_audio_stream,
                                                      self.close_audio_stream),
                          "custom": Mode_info('custom', "Custom", self.custom),
                          }
        self.color_generators = {
            "Static": self.color_generator_static,
            "Rainbow": self.color_generator_rainbow
        }
        self.gvars = GUI_variables(self)
        self.update_color_generator()
        self.mode_counter = self.mode_counter2 = 0
        self.e131 = E131Module(self.led_num)
        self.prev_mode = 'off'
        self.prev_audio_ratio = 0

    """
    ### setup functions
    """

    def clear_leds(self):
        self.set_leds(np.zeros(self.led_num))

    def setup_audio_stream(self):
        self.portaudio = audio_functions.pyaudio.PyAudio()
        self.audio_stream, self.audio_rate = audio_functions.start_audio_stream(self.portaudio,
                                                                                self.gvars.audio_device)
        self.past_states = np.zeros([self.led_num, 3])

    """
    ### RGB functions
    """

    def rainbow(self):
        data = np.array(
            [hsv2rgb(h % 256, 255, 255) for h in range(int(self.mode_counter), int(self.mode_counter + self.led_num))])
        data = data.flatten()
        self.set_leds(data)
        self.mode_counter += self.gvars.speed / 10

    def audio_static(self):
        audio_ratio, self.mode_counter, self.mode_counter2 = audio_functions.get_normalized_audio_level(
            self.audio_stream, self.mode_counter, self.mode_counter2)

        color = self.color_generator(audio_ratio)
        data = np.tile(audio_ratio * color,
                       self.led_num)  # get color of one pixel given the base color,then repeat
        self.set_leds(data)

    def audio_speakers(self):
        audio_ratio, self.mode_counter, self.mode_counter2 = audio_functions.get_normalized_audio_level(
            self.audio_stream, self.mode_counter, self.mode_counter2)

        color = self.color_generator(audio_ratio)

        # use self.past_states as a FIFO queue to store past states
        self.past_states = np.roll(self.past_states, 1, axis=0)
        self.past_states[0] = audio_ratio * color

        # calculate actual leds
        distances = self.interpolate_distance_from_speakers(np.arange(self.led_num))
        speed = max(self.gvars.speed * 5, 1)
        indices = distances / speed
        floored_indices = np.floor(indices).astype(int)
        partials = (indices - floored_indices).reshape([self.led_num, 1])
        colors = self.past_states[floored_indices] * (1 - partials) + self.past_states[floored_indices + 1] * partials
        self.set_leds(colors.flatten().astype(int))

    def audio_spectrum(self):
        samples = 8
        magnitudes = audio_functions.get_audio_spectrum(self.audio_stream, self.audio_rate, samples)

        # interpolate samples over all leds
        brightness_values = np.arange(self.led_num)
        for x, b in enumerate(brightness_values):
            i = b / self.led_num * (samples - 2) + 1
            floor_i = np.floor(i).astype(int)
            partial = i - floor_i
            brightness_values[x] = magnitudes[floor_i] * (1 - partial) + magnitudes[floor_i + 1] * partial

        brightness_values = np.clip((brightness_values - 350) / 16, 0, 255) / 4

        hues = np.linspace(0, 255, self.led_num)
        colors_hsv = np.vstack([brightness_values, 255 * np.ones(self.led_num), brightness_values]).T
        colors = np.array([np.array(np_hsv2rgb(led)) for led in colors_hsv])

        """import matplotlib.pyplot as plt
        plt.plot(np.arange(self.led_num), hues)
        plt.plot(np.arange(self.led_num), brightness_values)
        plt.show()
        return"""

        self.set_leds(colors.flatten().astype(int))

    def screen_mirroring(self):
        color = screen_average(self.gvars.svars)
        data = np.tile(color, self.led_num).flatten()
        self.set_leds(data)

    def custom(self):
        color1 = hsv2rgb(0,0,50)
        color2 = hsv2rgb(0,255,255)
        data = np.zeros((self.led_num, 3))
        data[68:185,:] = color1
        data[195:255,:] = color1
        data[265:, :] = color2

        self.set_leds(data.flatten())

    """
    ### close functions
    """

    def close_audio_stream(self):
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.portaudio.terminate()

    """
    ### color generators
    """

    def color_generator_static(self, audio_ratio=None):
        return self.gvars.color

    def color_generator_rainbow(self, audio_ratio=None) -> np.ndarray:
        if audio_ratio is not None:
            speed = max((audio_ratio - self.prev_audio_ratio) - 0.4, 0) * 800
            self.prev_audio_ratio = audio_ratio
        else:
            speed = self.gvars.speed
        self.hue_shift = (self.hue_shift + speed / 10) % 256
        color = hsv2rgb(int(self.hue_shift), 255, 255)
        return color

    """
    ### other functions
    """

    def display_mode(self, mode: str = 'off'):
        # stop previous function
        self.e131.set_rgb_function(lambda: None)

        # run close function of the previous mode
        self.mode_list[self.prev_mode].close_function()

        self.mode_counter = 0
        self.args = []

        # run mode's setup_function (do nothing if it's not defined)
        self.mode_list[mode].setup_function()

        # sets RGB function as data generator for the e131 module
        self.e131.set_rgb_function(self.mode_list[mode].RGBfunction)

    def get_modes(self):
        return self.mode_list.values()

    def set_led_number(self, led_number: int):
        self.led_num = led_number
        self.e131.set_led_number(led_number)

    def update_color_generator(self):
        if self.gvars.color_generator_name is not None:
            self.color_generator = self.color_generators[self.gvars.color_generator_name]

    def set_leds(self, data: np.ndarray):
        # cap brightness
        self.e131.send_data(data * min(self.gvars.brightness, 100) / 100)

    def interpolate_distance_from_speakers(self, x):
        return np.clip(np.minimum(abs(x - self.gvars.speaker1), abs(x - self.gvars.speaker2)), 0,
                       self.led_num - 2)  # clipped to led_num-2 to avoid IndexError in audio_speakers when speed = 0

    def set_ip(self):
        """
        set the ip stored inside the gvars object. Prints error message on console if IP is not valid
        """
        if all(x is not None for x in self.gvars.ip):
            ip = list(map(lambda intvar: intvar, self.gvars.ip))
            if all(0 <= x < 256 for x in ip):
                self.e131.set_ip('.'.join(map(str, ip)))
                self.gvars.print_console("IP address updated")
            else:
                self.gvars.print_console(str("invalid ip address: " + '.'.join(map(str, ip))))
        else:
            self.gvars.print_console("invalid ip address: " + '.'.join(map(str, self.gvars.ip)))
