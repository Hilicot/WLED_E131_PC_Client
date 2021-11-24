from PIL import ImageGrab
import numpy as np
from utils import rgb2hsv, hsv2rgb
from gui import GUI_variables

# TODO provo a usare https://sighack.com/post/averaging-rgb-colors-the-right-way.
#  Inoltre, il prodotto finale potrebbe avere come impostazioni la scelta tra detection statica,
#  oppure con colori diversi a sinistra/destra (multi zona).
#  poi l'utente deve anche scegliere la risoluzione/area da catturare

w = 1920
h = 1080


def screen_average(gvars: GUI_variables) -> np.ndarray:
    """
    Calculate screen average by simply averaging all pixels
    :param gvars:
    :return:
    """
    screen = np.array(ImageGrab.grab(bbox=(gvars.capture_x_offset.get(), gvars.capture_y_offset.get(),
                                           gvars.capture_width.get()+gvars.capture_x_offset.get(),
                                           gvars.capture_height.get()+gvars.capture_y_offset.get())))

    avg = np.mean(screen, axis=(0, 1)).astype(np.uint8)
    hsv = rgb2hsv(*avg)
    rgb = hsv2rgb(hsv[0], min(hsv[1] + 25, 255), hsv[2])
    return rgb
