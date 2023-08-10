from PIL import ImageGrab
import numpy as np
from utils import rgb2hsv, hsv2rgb
from gui import ScreenVariables, ScreenMode

# TODO il prodotto finale potrebbe avere come impostazioni la scelta tra detection statica,
#  oppure con colori diversi a sinistra/destra (multi zona).

def screen_average(svars: ScreenVariables) -> np.ndarray:
    """
    Calculate screen average by simply averaging all pixels
    :param svars: ScreenVariables object, containing all the info about the currently active screen
    :return: a RGB representation of the average screen color
    """

    # fetch screen data
    # TODO try implementing in C code to see if it run faster
    bbox = None if svars.fullscreen else (svars.capture_x_offset, svars.capture_y_offset,
                                          svars.capture_width + svars.capture_x_offset,
                                          svars.capture_height + svars.capture_y_offset)
    screen = np.array(ImageGrab.grab(bbox=bbox))

    # Handle different screen modes
    if svars.screen_mode == ScreenMode.Fast:  # calculate average considering only a part of the pixels
        avg = np.mean(screen[::ScreenMode.FastRatio, ::ScreenMode.FastRatio, :], axis=(0, 1)).astype(np.uint8)

    elif svars.screen_mode == ScreenMode.SquaredAverage:    # calculate average of squared RGB values
        avg = np.sqrt(np.mean(np.square(screen.astype(np.uint16)), axis=(0, 1))).astype(np.uint8)

    else:   # calculate regular average of all pixels
        avg = np.mean(screen, axis=(0, 1)).astype(np.uint8)

    # boost saturation
    hsv = rgb2hsv(*avg)
    rgb = hsv2rgb(hsv[0], min(hsv[1] + int(svars.saturation_boost), 255), hsv[2])

    return rgb
