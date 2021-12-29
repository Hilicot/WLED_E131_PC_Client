from PyQt5.QtWidgets import QApplication
from RGB_effects import *
from gui import GUI_variables, ApplicationGUI
from audio_functions import list_available_audio_devices
import sys

if __name__ == '__main__':
    rgb_effects = RGBEffects()
    gvars = rgb_effects.gvars

    app = QApplication(sys.argv)
    gallery = ApplicationGUI(rgb_effects)
    gallery.show()
    sys.exit(app.exec_())
