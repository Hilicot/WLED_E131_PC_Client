from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QDialog, QStyleFactory, QVBoxLayout, QLabel

from .tab_general import TabGeneral
from .tab_screen_mirroring import TabScreen

# FIXME close button not working
class ApplicationGUI(QDialog):

    def __init__(self, rgb_effects, parent=None):
        super(ApplicationGUI, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.setWindowTitle("E131 RGB controller")
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        # TODO add possibiliy to chose dark fusion palette (google for it)
        QApplication.setPalette(QApplication.style().standardPalette())
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab_general = TabGeneral(self, rgb_effects)
        self.tab_screen = TabScreen(self, rgb_effects)

        self.tabs.addTab(self.tab_general, "General")
        self.tabs.addTab(self.tab_screen, "Screen Mirroring")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

