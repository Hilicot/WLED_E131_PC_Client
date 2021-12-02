from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QRadioButton, QComboBox, \
    QColorDialog, QPushButton, QStyleFactory, QGroupBox, QSpinBox,QSlider
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from .GUI_variables import GUI_variables, WidgetSubdomain, update_widgets
import numpy as np


class TabGeneral(QWidget):
    topLeftGroupBox = None
    topRightGroupBox = None
    bottomGroupBox = None

    ColorPickerBtn = None

    def __init__(self, parent, rgb_effects):
        super(TabGeneral, self).__init__(parent)
        self.rgb_effects = rgb_effects

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomGroupBox()

        tabLayout = QGridLayout()
        tabLayout.addWidget(self.topLeftGroupBox, 0, 0)
        tabLayout.addWidget(self.topRightGroupBox, 0, 1)
        tabLayout.addWidget(self.bottomGroupBox, 1, 0, 1, 2)

        self.setLayout(tabLayout)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("RGB mode:")
        RGBSelectionRadio = []
        for m in self.rgb_effects.get_modes():
            RGBSelectionRadio.append(QRadioButton(m.label))
        RGBSelectionRadio[0].setChecked(True)

        topLeft = QVBoxLayout()
        for radioBtn in RGBSelectionRadio:
            topLeft.addWidget(radioBtn)
        topLeft.addStretch(1)
        self.topLeftGroupBox.setLayout(topLeft)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Color:")
        ColorGenerator = QComboBox()
        ColorGenerator.addItems(self.rgb_effects.color_generators.keys())
        self.ColorPickerBtn = QPushButton("")
        self.ColorPickerBtn.setToolTip("Change base color")
        self.ColorPickerBtn.clicked.connect(lambda: self.pick_color(rgb_effects.gvars))
        self.ColorPickerBtn.setStyleSheet("* { background-color: " + self.rgb_effects.gvars.color_hex + "}")
        if "Windows" in QStyleFactory.keys():
            self.ColorPickerBtn.setStyle(QStyleFactory.create("Windows"))

        topRight = QVBoxLayout()
        topRight.addWidget(ColorGenerator)
        topRight.addWidget(self.ColorPickerBtn)
        topRight.addStretch(1)
        self.topRightGroupBox.setLayout(topRight)

    def createBottomGroupBox(self):
        self.bottomGroupBox = QGroupBox("Global Options:")
        LedNumLabel = QLabel("Led Number")
        LedNumEntry = QSpinBox()
        LedNumEntry.setMinimum(1)
        LedNumEntry.setMaximum(1500)
        LedNumEntry.setValue(300)
        LedNumEntry.setToolTip("Specify the number of leds to drive")
        Speaker1Label = QLabel("Speaker 1")
        Speaker1Entry = QSpinBox()
        Speaker1Label.setToolTip(
            "Position of the first emulated speaker for Audio Visualization (must be a the index of an existing LED)")
        Speaker1Entry.setMinimum(0)
        Speaker1Entry.setMaximum(1500)
        Speaker1Entry.setValue(0)
        Speaker2Label = QLabel("Speaker 2")
        Speaker2Entry = QSpinBox()
        Speaker2Label.setToolTip(
            "Position of the second emulated speaker for Audio Visualization (must be a the index of an existing LED)")
        Speaker2Entry.setMinimum(0)
        Speaker2Entry.setMaximum(1500)
        Speaker2Entry.setValue(0)

        BrightnessIcon = QLabel('<html><img src="gui/icons/lightbulb24"></html>')
        BrightnessSlider = QSlider(Qt.Vertical)
        BrightnessSlider.setValue(40)
        SpeedIcon = QLabel('<html><img src="gui/icons/deadline24"></html>')
        SpeedSlider = QSlider(Qt.Vertical)
        SpeedSlider.setMaximum(500)
        SpeedSlider.setValue(10)

        bottomLayout = QGridLayout()
        bottomLayout.addWidget(LedNumLabel, 0, 0)
        bottomLayout.addWidget(LedNumEntry, 0, 1)
        bottomLayout.addWidget(Speaker1Label,1,0)
        bottomLayout.addWidget(Speaker1Entry, 1, 1)
        bottomLayout.addWidget(Speaker2Label, 2, 0)
        bottomLayout.addWidget(Speaker2Entry, 2,1)
        bottomLayout.addWidget(BrightnessSlider, 0, 2, 2, 1)
        bottomLayout.addWidget(BrightnessIcon, 2, 2)
        bottomLayout.addWidget(SpeedSlider, 0, 3, 2, 1)
        bottomLayout.addWidget(SpeedIcon, 2, 3)
        self.bottomGroupBox.setLayout(bottomLayout)

    def pick_color(self, gvars: GUI_variables):
        color = QColorDialog.getColor()
        gvars.color = np.array(color.getRgb())[:3]
        gvars.color_hex = color.name()
        # update color of color picker button
        self.ColorPickerBtn.setStyleSheet("* { background-color: " + gvars.color_hex + "}")


# TODO remove
def draw_tab_general(rgb_effects, tab, row=0):
    gvars = rgb_effects.gvars

    tab1_top_frame = Frame(master=tab)
    tab1_top_frame.grid(row=0, column=0, sticky=(W, N), padx=(5, 10))
    gvars.mode = StringVar(tab, 'off')

    """
            Modes
    """
    tk.Label(tab1_top_frame, text='RGB mode:').grid(row=row, column=0, sticky=(W, N))
    row += 1
    mode_radio_btns = []
    for m in rgb_effects.get_modes():
        radio_btn = tk.Radiobutton(master=tab1_top_frame, text=m.label, variable=gvars.mode, value=m.name,
                                   command=lambda: update_widgets(gvars, gvars.root,
                                                                  lambda: rgb_effects.display_mode(gvars.mode.get())))
        radio_btn.grid(row=row, column=0, sticky=W, padx=(15, 0))
        mode_radio_btns.append(radio_btn)
        row += 1

    """
            Color Generators
    """
    row_temp = 0
    tk.Label(tab1_top_frame, text='Color:').grid(row=row_temp, column=4, sticky=(W, N))
    row_temp += 1
    gvars.color_generator_name = StringVar(tab1_top_frame, "Rainbow")
    rgb_effects.update_color_generator()
    for gen in rgb_effects.color_generators.keys():
        tk.Radiobutton(master=tab1_top_frame, text=gen, variable=gvars.color_generator_name, value=gen,
                       command=rgb_effects.update_color_generator).grid(row=row_temp, column=4, sticky=W, padx=(15, 0))
        row_temp += 1

    """
            #
            #           OPTIONS
            #

    """
    gray = '#fafafa'
    gray_frame = Frame(master=tab, background=gray)
    gray_frame['borderwidth'] = 1
    gray_frame['relief'] = 'groove'
    gray_frame.grid(row=row, column=0, padx=(5, 5), pady=(10, 10))
    row += 1
    tk.Label(gray_frame, text='Global Options:', background=gray).grid(row=row, column=0, sticky=(W, E))
    row += 1
    options_frame = Frame(master=gray_frame, background=gray)
    options_frame.grid(row=row, column=0, padx=(10, 10), pady=(10, 0))

    """
            Num_leds + color
    """
    gvars.num_leds = IntVarSafe(options_frame, 300)
    tk.Label(options_frame, text="Led number", background=gray).grid(row=row, column=0, sticky=(W, E))
    gvars.num_leds.trace_add("write", lambda a, b, c: rgb_effects.set_led_number(gvars.num_leds.get()))
    tk.Entry(options_frame, text=gvars.num_leds, width=10, ).grid(row=row, column=1,
                                                                  sticky=(W, E))
    # add white space
    tk.Label(options_frame, text="", background=gray, width=10).grid(row=row, column=3, sticky=(W, E))

    # color picker:
    tk.Label(options_frame, text="Color", background=gray).grid(row=row, column=4, sticky=W)
    color_button = Button(options_frame, command=lambda: gvars.choose_color(color_button), background=gvars.color_hex,
                          width=5)
    color_button.grid(row=row, column=5)

    row += 1

    """
    #       Brightness + Speed
    """
    # TODO switch to sliders instead of IntEntry
    gvars.brightness = IntVarSafe(options_frame, 40)
    tk.Label(options_frame, text="Brightness (max 100)", background=gray).grid(row=row, column=0, sticky=(W, E))
    tk.Entry(master=options_frame, text=gvars.brightness, width=10).grid(row=row, column=1, sticky=(W, E))

    gvars.speed = IntVarSafe(options_frame, 10)
    tk.Label(options_frame, text="Speed", background=gray).grid(row=row, column=4, sticky=(W, E))
    tk.Entry(master=options_frame, text=gvars.speed, width=10).grid(row=row, column=5, sticky=(W, E))

    row += 1

    """
    #       Speakers
    """

    gvars.speaker1 = IntVarSafe(options_frame, 0)
    gvars.speaker2 = IntVarSafe(options_frame, 0)
    tk.Label(options_frame, text="Speaker1", background=gray).grid(row=row, column=0, sticky=(W, E))
    tk.Entry(master=options_frame, text=gvars.speaker1, width=10).grid(row=row, column=1, sticky=(W, E))
    tk.Label(options_frame, text="Speaker2", background=gray).grid(row=row, column=4, sticky=(W, E))
    tk.Entry(master=options_frame, text=gvars.speaker2, width=10).grid(row=row, column=5, sticky=(W, E))

    row += 1

    """
    #       Ip address
    """

    gvars.ip[0] = IntVarSafe(options_frame, 192)
    gvars.ip[1] = IntVarSafe(options_frame, 168)
    gvars.ip[2] = IntVarSafe(options_frame, 1)
    gvars.ip[3] = IntVarSafe(options_frame, 213)
    ip_frame = Frame(master=gray_frame, background=gray)
    ip_frame.grid(row=row, column=0, sticky=(N, W, E, S), padx=(10, 10), pady=(10, 0))
    tk.Label(ip_frame, text="IP", background=gray, width=12).grid(row=0, column=0, sticky=W)
    tk.Entry(ip_frame, text=gvars.ip[0], width=6).grid(row=0, column=1, sticky=W)
    tk.Entry(ip_frame, text=gvars.ip[1], width=6).grid(row=0, column=2, sticky=W)
    tk.Entry(ip_frame, text=gvars.ip[2], width=6).grid(row=0, column=3, sticky=W)
    tk.Entry(ip_frame, text=gvars.ip[3], width=6).grid(row=0, column=4, sticky=W)
    Button(ip_frame, text="Update", command=rgb_effects.set_ip).grid(row=0, column=5, sticky=W)

    row += 1
    """
    #       Audio device
    """

    devices, default_device = gvars.list_available_audio_devices()
    gvars.audio_device = StringVar(options_frame, default_device)
    audio_device_frame = Frame(master=gray_frame, background=gray)
    audio_device_frame.grid(row=row, column=0, sticky=(N, W, E, S), padx=(10, 10), pady=(0, 10))
    tk.Label(audio_device_frame, text="Audio device", background=gray).grid(row=0, column=0, sticky=(W, E))
    tk.OptionMenu(audio_device_frame, gvars.audio_device, default_device, *devices).grid(row=0, column=1, sticky=(W, E))

    row += 1
