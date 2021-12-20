from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QRadioButton, QComboBox, \
    QColorDialog, QPushButton, QStyleFactory, QGroupBox, QSpinBox, QSlider
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from .GUI_variables import GUI_variables
import numpy as np


class TabGeneral(QWidget):
    topLeftGroupBox = None
    topRightGroupBox = None
    bottomGroupBox = None

    ColorPickerBtn = None

    def __init__(self, parent, rgb_effects):
        super(TabGeneral, self).__init__(parent)
        self.rgb_effects = rgb_effects
        self.RGBSelectionRadio = []

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
        for m in self.rgb_effects.get_modes():
            radio_item = QRadioButton(m.label)
            radio_item.clicked.connect(self.updateMode)
            self.RGBSelectionRadio.append((radio_item, m.name))

        self.RGBSelectionRadio[0][0].setChecked(True)

        topLeft = QVBoxLayout()
        for radioBtn in self.RGBSelectionRadio:
            topLeft.addWidget(radioBtn[0])
        topLeft.addStretch(1)
        self.topLeftGroupBox.setLayout(topLeft)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Color:")
        ColorGenerator = QComboBox()
        ColorGenerator.addItems(self.rgb_effects.color_generators.keys())
        self.ColorPickerBtn = QPushButton("")
        self.ColorPickerBtn.setToolTip("Change base color")
        self.ColorPickerBtn.clicked.connect(lambda: self.pick_color(self.rgb_effects.gvars))
        self.ColorPickerBtn.setStyleSheet("* { background-color: " + self.rgb_effects.gvars.color_hex + "}")
        # set button style to "Windows" to avoid Fusion's colored overlay
        if "Windows" in QStyleFactory.keys():
            self.ColorPickerBtn.setStyle(QStyleFactory.create("Windows"))

        topRight = QVBoxLayout()
        topRight.addWidget(ColorGenerator)
        topRight.addWidget(self.ColorPickerBtn)
        topRight.addStretch(1)
        self.topRightGroupBox.setLayout(topRight)

    def createBottomGroupBox(self):
        gvars: GUI_variables = self.rgb_effects.gvars
        self.bottomGroupBox = QGroupBox("Global Options:")
        LedNumLabel = QLabel("Led Number")
        LedNumEntry = QSpinBox()
        LedNumEntry.setMinimum(1)
        LedNumEntry.setMaximum(1500)
        LedNumEntry.setValue(gvars.num_leds)
        LedNumEntry.setToolTip("Specify the number of leds to drive")
        LedNumEntry.valueChanged.connect(lambda: gvars.setNumLeds(LedNumLabel.value))
        Speaker1Label = QLabel("Speaker 1")
        Speaker1Entry = QSpinBox()
        Speaker1Label.setToolTip(
            "Position of the first emulated speaker for Audio Visualization (must be a the index of an existing LED)")
        Speaker1Entry.setMinimum(0)
        Speaker1Entry.setMaximum(1500)
        Speaker1Entry.setValue(gvars.speaker1)
        Speaker1Entry.valueChanged.connect(lambda: gvars.setSpeaker1(Speaker1Entry.value))
        Speaker2Label = QLabel("Speaker 2")
        Speaker2Entry = QSpinBox()
        Speaker2Label.setToolTip(
            "Position of the second emulated speaker for Audio Visualization (must be a the index of an existing LED)")
        Speaker2Entry.setMinimum(0)
        Speaker2Entry.setMaximum(1500)
        Speaker2Entry.setValue(gvars.speaker1)
        Speaker2Entry.valueChanged.connect(lambda: gvars.setSpeaker2(Speaker2Entry.value))

        BrightnessIcon = QLabel('<html><img src="gui/icons/lightbulb24"></html>')
        BrightnessSlider = QSlider(Qt.Vertical)
        BrightnessSlider.setValue(gvars.brightness)
        BrightnessSlider.valueChanged.connect(lambda: gvars.setBrightness(BrightnessSlider.value))
        SpeedIcon = QLabel('<html><img src="gui/icons/deadline24"></html>')
        SpeedSlider = QSlider(Qt.Vertical)
        SpeedSlider.setMaximum(500)
        SpeedSlider.setValue(gvars.speed)
        SpeedSlider.valueChanged.connect(lambda: gvars.setSpeed(SpeedSlider.value))

        AudioDeviceLabel = QLabel("Audio Device")
        AudioDeviceDropdown = QComboBox()
        devices, default_device, default_device_id = gvars.list_available_audio_devices()
        AudioDeviceDropdown.addItems(devices)
        AudioDeviceDropdown.setCurrentIndex(default_device_id)
        gvars.audio_device = default_device
        AudioDeviceDropdown.currentIndexChanged.connect(
            lambda: gvars.setAudioDeviceFromIndex(AudioDeviceDropdown.currentIndex()))

        bottomLayout = QGridLayout()
        bottomLayout.addWidget(LedNumLabel, 0, 0)
        bottomLayout.addWidget(LedNumEntry, 0, 1)
        bottomLayout.addWidget(Speaker1Label, 1, 0)
        bottomLayout.addWidget(Speaker1Entry, 1, 1)
        bottomLayout.addWidget(Speaker2Label, 2, 0)
        bottomLayout.addWidget(Speaker2Entry, 2, 1)
        bottomLayout.addWidget(BrightnessSlider, 0, 2, 2, 1)
        bottomLayout.addWidget(BrightnessIcon, 2, 2)
        bottomLayout.addWidget(SpeedSlider, 0, 3, 2, 1)
        bottomLayout.addWidget(SpeedIcon, 2, 3)
        bottomLayout.addWidget(AudioDeviceLabel, 3, 0)
        bottomLayout.addWidget(AudioDeviceDropdown, 3, 1)
        self.bottomGroupBox.setLayout(bottomLayout)

    def pick_color(self, gvars: GUI_variables):
        color = QColorDialog.getColor()
        gvars.color = np.array(color.getRgb())[:3]
        gvars.color_hex = color.name()
        # update color of color picker button
        self.ColorPickerBtn.setStyleSheet("* { background-color: " + gvars.color_hex + "}")

    def updateMode(self):
        # get the mode
        mode = 'off'
        for i, radio in enumerate(self.RGBSelectionRadio):
            if radio[0].isChecked():
                mode = radio[1]
                break
        self.rgb_effects.gvars.setMode(self.rgb_effects, mode)
