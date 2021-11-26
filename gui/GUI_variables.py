from tkinter import TclError, IntVar
from tkinter.colorchooser import askcolor
import numpy as np


class IntVarSafe(IntVar):
    """Variant of IntVar which never throws errors, but silently sets itself to zero"""

    def get(self):
        try:
            return super().get()
        except TclError:
            return 0


class GUI_variables:
    # General tab variables
    root = None
    mode = None
    widget_subdomains = dict()
    color_generator_name = None
    console_output = None
    num_leds = None
    speed = None
    audio_device = None
    color = np.array([255, 0, 0])
    color_hex = "#ff0000"
    hue = 0
    speaker1 = speaker2 = None
    brightness = None
    ip = [None, None, None, None]

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


class WidgetSubdomain:
    def __init__(self, controller_widget, enabled_value):
        self.enabled_value = enabled_value
        self.controller_widget = controller_widget

    def isEnabled(self) -> bool:
        return self.controller_widget.get() == self.enabled_value


def update_widgets(gvars: GUI_variables, root_widget, starting_function=lambda: None, enable=True):
    """
    Recursively descend in the widget tree from the starting_widget down. Each time a WidgetSubdomain is met,
    set all it's children to enabled or disabled based on their condition

    :param gvars:
    :param root_widget: the search starts from this widget
    :param starting_function: function to execute at the start. Can be unrelated, it's just handy for function chaining
    :param enable: if True enables all widgets, else disables them
    """
    starting_function()

    for w in root_widget.winfo_children():
        if w in gvars.widget_subdomains:
            subdom = gvars.widget_subdomains[w]
            update_widgets(gvars, w, enable=enable and subdom.isEnabled())
        elif "state" in w.keys():
            if enable:
                w["state"] = "normal"
            else:
                w["state"] = "disabled"
        elif len(w.winfo_children()) > 0:
            update_widgets(gvars, w, enable=enable)
