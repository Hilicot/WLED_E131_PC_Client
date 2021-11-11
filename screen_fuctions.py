from PIL import ImageGrab
import numpy as np
import cv2  # FIXME remove
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

        


def test():
    coef = 4

    if True:
        while True:
            import time
            screen = np.array(ImageGrab.grab(bbox=(200, 200, h, w)))

            quantized = screen//coef
            quantized *= coef
            avg = np.mean(screen, axis=(0,1)).astype(np.uint8)
            avg_pic = avg.reshape([1,1,3])
            hsv = cv2.cvtColor(avg_pic, cv2.COLOR_RGB2HSV)
            hsv[0][0][1] = min(hsv[0][0][1]+50,255)
            rgb_pic = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
            color_box = np.tile(rgb_pic[0][0],500*500).reshape([500,500,3])

            #cv2.imshow('window', color_box)
            cv2.imshow('window', cv2.cvtColor(np.tile(avg_pic,500*500).reshape([500,500,3]), cv2.COLOR_BGR2RGB))
            cv2.imshow('window_enhanced', cv2.cvtColor(color_box, cv2.COLOR_BGR2RGB))

            kmeans()

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    else:
        kmeans()

