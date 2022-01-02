from PIL import ImageGrab
import numpy as np
from utils import rgb2hsv, hsv2rgb
from gui import ScreenVariables

# TODO il prodotto finale potrebbe avere come impostazioni la scelta tra detection statica,
#  oppure con colori diversi a sinistra/destra (multi zona).

w = 1920
h = 1080


def screen_average(svars: ScreenVariables) -> np.ndarray:
    """
    Calculate screen average by simply averaging all pixels
    :param svars:
    :return:
    """

    # TODO try implementing in C code to see if it run faster
    # TODO implement FullScreen
    screen = np.array(ImageGrab.grab(bbox=(svars.capture_x_offset, svars.capture_y_offset,
                                           svars.capture_width + svars.capture_x_offset,
                                           svars.capture_height + svars.capture_y_offset)))

    if svars.screen_mode == "Fast":  # calculate average considering only a part of the pixels
        avg = np.mean(screen[::8, ::8, :], axis=(0, 1)).astype(np.uint8)
    elif svars.screen_mode == "Squared Average":
        avg = np.sqrt(np.mean(np.square(screen.astype(np.uint16)), axis=(0, 1))).astype(np.uint8)
    else:
        avg = np.mean(screen, axis=(0, 1)).astype(np.uint8)

    # boost saturation
    hsv = rgb2hsv(*avg)
    rgb = hsv2rgb(hsv[0], min(hsv[1] + 50, 255), hsv[2])

    return rgb
