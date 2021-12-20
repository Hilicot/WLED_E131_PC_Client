from PyQt5.QtWidgets import QApplication,QWidget,QTabWidget,QDialog,QStyleFactory,QVBoxLayout,QLabel

from .tab_general import TabGeneral
from .footer import draw_footer


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
        self.tab_screen = QWidget()

        self.tabs.addTab(self.tab_general,"General")
        self.tabs.addTab(self.tab_screen, "Screen Mirroring")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

"""
def draw_GUI(rgb_effects):
    root = Tk()
    root.title("E131 RGB controller")
    rgb_effects.gvars.root = root
    tabControl = tk.Notebook(root)

    tab1 = tk.Frame(tabControl)
    tabControl.add(tab1, text='General')
    draw_tab_general(rgb_effects, tab1)

    tab2 = tk.Frame(tabControl)
    tabControl.add(tab2, text='Screen Mirroring')
    draw_tab_screen_mirroring(rgb_effects, tab2)

    tabControl.grid(row=0, column=0)

    draw_footer(rgb_effects, root, 1)

    rgb_effects.set_ip()
    rgb_effects.gvars.print_console("Ready")
    update_widgets(rgb_effects.gvars, root)

    return root"""
