from PIL import ImageGrab
import numpy as np
from utils import rgb2hsv,hsv2rgb

# TODO provo a usare il k-means / mean-shift.
#  Il prodotto finale potrebbe avere come impostazioni la scelta tra detection statica,
#  oppure con colori diversi a sinistra/destra (multi zona).
#  poi l'utente deve anche scegliere la risoluzione/area da catturare

w = 1200
h = 800

def screen_average() -> np.ndarray:
    screen = np.array(ImageGrab.grab(bbox=(200, 200, 800, 600)))

    avg = np.mean(screen, axis=(0, 1)).astype(np.uint8)
    hsv = rgb2hsv(*avg)
    rgb = hsv2rgb(hsv[0],min(hsv[1]+25,255),hsv[2])
    return rgb


