from PIL import ImageGrab
import numpy as np
from utils import rgb2hsv, hsv2rgb
from gui import GUI_variables

# TODO il prodotto finale potrebbe avere come impostazioni la scelta tra detection statica,
#  oppure con colori diversi a sinistra/destra (multi zona).

w = 1920
h = 1080


def screen_average(gvars: GUI_variables) -> np.ndarray:
    """
    Calculate screen average by simply averaging all pixels
    :param gvars:
    :return:
    """

    #TODO try implementing in C code to see if it run faster (then remove timer code)
    dbg = False
    if dbg:
        from time import time
        start = time()
    screen = np.array(ImageGrab.grab(bbox=(gvars.capture_x_offset.get(), gvars.capture_y_offset.get(),
                                           gvars.capture_width.get()+gvars.capture_x_offset.get(),
                                           gvars.capture_height.get()+gvars.capture_y_offset.get())))

    if gvars.screen_mode.get() == "Fast":   # calculate average considering only a part of the pixels
        avg = np.mean(screen[::8,::8,:], axis=(0, 1)).astype(np.uint8)
    elif gvars.screen_mode.get() == "Squared Average":
        avg = np.sqrt(np.mean(np.square(screen.astype(np.uint16)), axis=(0, 1))).astype(np.uint8)
    else:
        avg = np.mean(screen, axis=(0, 1)).astype(np.uint8)

    # boost saturation
    hsv = rgb2hsv(*avg)
    rgb = hsv2rgb(hsv[0], min(hsv[1] + 50, 255), hsv[2])

    if dbg: print(time()-start)

    return rgb
