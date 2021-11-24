from utils import *
from typing import Dict, List
from E131Module import E131Module
import audio_functions
from screen_fuctions import screen_average


class RGBEffects:
    led_num = 300
    audio_stream = None
    audio_rate = 0
    portaudio = None
    hue_shift = 0
    color_generator = lambda x: None
    past_states = None

    # TODO audio_spectrum
    def __init__(self, gui_variables):
        self.mode_list = {'off': Mode_info('off', 'off', lambda: None, setup_function=self.clear_leds),
                          "rainbow": Mode_info('rainbow', "Rainbow", self.rainbow),
                          "screen_mirroring": Mode_info("screen_mirroring", 'Screen Mirroring', self.screen_mirroring),
                          "audio_static": Mode_info("audio_static", 'Audio Visualizer (Static)',
                                                    self.audio_static, self.setup_audio_stream,
                                                    self.close_audio_stream),
                          "audio_speakers": Mode_info("audio_speakers", 'Audio Visualizer (Speakers)',
                                                      self.audio_speakers, self.setup_audio_stream,
                                                      self.close_audio_stream)
                          }
        self.color_generators = {
            "Static": self.color_generator_static,
            "Rainbow": self.color_generator_rainbow
        }
        self.gvars = gui_variables
        self.update_color_generator()
        self.mode_counter = self.mode_counter2 = 0
        self.e131 = E131Module(self.led_num)
        self.prev_mode = 'off'

    """
    ### setup functions
    """

    def clear_leds(self):
        self.set_leds(np.zeros(self.led_num))

    def setup_audio_stream(self):
        self.portaudio = audio_functions.pyaudio.PyAudio()
        self.audio_stream, self.audio_rate = audio_functions.start_audio_stream(self.portaudio,
                                                                                self.gvars.audio_device.get())
        self.past_states = np.zeros([self.led_num, 3])

    """
    ### RGB functions
    """

    def rainbow(self):
        data = np.array(
            [hsv2rgb(h%256, 255, 255) for h in range(int(self.mode_counter), int(self.mode_counter + self.led_num))])
        data = data.flatten()
        self.set_leds(data)
        self.mode_counter += self.gvars.speed.get()/10

    def audio_static(self):
        audio_ratio, self.mode_counter, self.mode_counter2 = audio_functions.get_normalized_audio_level(
            self.audio_stream, self.mode_counter, self.mode_counter2)
        color = self.color_generator()
        data = np.tile(audio_ratio*color,
                       self.led_num)  # get color of one pixel given the base color,then repeat
        self.set_leds(data)

    def audio_speakers(self):
        audio_ratio, self.mode_counter, self.mode_counter2 = audio_functions.get_normalized_audio_level(
            self.audio_stream, self.mode_counter, self.mode_counter2)

        color = self.color_generator()

        # use self.past_states as a FIFO queue to store past states
        self.past_states = np.roll(self.past_states, 1, axis=0)
        self.past_states[0] = audio_ratio*color

        # calculate actual leds
        distances = self.interpolate_distance_from_speakers(np.arange(self.led_num))
        indices = (distances*self.gvars.speed.get()/10).astype(int)
        self.set_leds(self.past_states[indices].flatten())

    def screen_mirroring(self):
        color = screen_average(self.gvars)
        data = np.tile(color,self.led_num).flatten()
        self.set_leds(data)


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

    def color_generator_static(self):
        return self.gvars.color

    def color_generator_rainbow(self) -> np.ndarray:
        color = hsv2rgb(int(self.hue_shift), 255, 255)
        self.hue_shift = (self.hue_shift + self.gvars.speed.get()/10)%256
        return color

    """
    ### other functions
    """

    def display_mode(self, mode: str = 'off'):
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
            self.color_generator = self.color_generators[self.gvars.color_generator_name.get()]

    def set_leds(self, data: np.ndarray):
        # cap brightness
        self.e131.send_data(data*min(self.gvars.brightness.get(), 100)/100)

    def interpolate_distance_from_speakers(self, x):
        return np.minimum(abs(x - self.gvars.speaker1.get()), abs(x - self.gvars.speaker2.get()))

    def set_ip(self):
        """
        set the ip stored inside the gvars object. Prints error message on console if IP is not valid
        """
        if all(x is not None for x in self.gvars.ip):
            ip = list(map(lambda intvar:intvar.get(), self.gvars.ip))
            if all(0<=x<256 for x in ip):
                self.e131.set_ip('.'.join(map(str,ip)))
                self.gvars.print_console("IP address updated")
            else:
                self.gvars.print_console(str("invalid ip address: "+'.'.join(map(str,ip))))
        else:
            self.gvars.print_console("invalid ip address: " + '.'.join(map(str,self.gvars.ip)))
