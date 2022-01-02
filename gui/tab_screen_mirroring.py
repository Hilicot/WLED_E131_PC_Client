from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QRadioButton, QComboBox, \
    QColorDialog, QPushButton, QStyleFactory, QGroupBox, QSpinBox, QSlider, QCheckBox, QApplication
from PyQt5.QtCore import Qt

from .GUI_variables import ScreenVariables


class TabScreen(QWidget):
    topLeftGroupBox = None
    topRightGroupBox = None
    bottomGroupBox = None

    ColorPickerBtn = None

    def __init__(self, parent, rgb_effects):
        super(TabScreen, self).__init__(parent)
        self.rgb_effects = rgb_effects
        svars: ScreenVariables = rgb_effects.gvars.svars

        ####
        # WIDGETS
        ####

        ActiveCheckbox = QCheckBox("Screen Mirroring")
        ActiveCheckbox.stateChanged.connect(self.activateScreenRecording)

        self.OptionsBox = QGroupBox()

        ScreenModeLabel = QLabel("Mode")
        ScreenModeDropdown = QComboBox()
        ScreenModeDropdown.addItems(["Average", "Squared Average", "Fast"])
        ScreenModeDropdown.setCurrentText('Average')
        ScreenModeDropdown.currentIndexChanged.connect(svars.setScreenMode)

        FullscreenCheckbox = QCheckBox("Fullscreen")
        FullscreenCheckbox.stateChanged.connect(lambda state: svars.setFullScreen(state == Qt.Checked))

        # TODO set default capture area based on screen size
        """
        screen_size = QApplication(argv)
        screen_size = QApplication(argv).screen_size.desktop().screenGeometry()
"""
        WidthLabel = QLabel("Width")
        WidthEntry = QSpinBox()
        WidthEntry.setMinimum(1)
        WidthEntry.setMaximum(1920)
        WidthEntry.setValue(svars.capture_width)
        WidthEntry.setToolTip("Insert the width (in pixels) of the capture area")
        WidthEntry.valueChanged.connect(svars.setWidth)
        HeightLabel = QLabel("Height")
        HeightEntry = QSpinBox()
        HeightEntry.setMinimum(1)
        HeightEntry.setMaximum(1080)
        HeightEntry.setValue(svars.capture_width)
        HeightEntry.setToolTip("Insert the height (in pixels) of the capture area")
        HeightEntry.valueChanged.connect(svars.setHeight)
        XOffsetLabel = QLabel("X offset")
        XOffsetEntry = QSpinBox()
        XOffsetEntry.setMinimum(0)
        XOffsetEntry.setMaximum(1920 - 1)
        XOffsetEntry.setValue(svars.capture_x_offset)
        XOffsetEntry.setToolTip("Horizontal offset (in pixels) from the left edge of the screen")
        XOffsetEntry.valueChanged.connect(svars.setXOffset)
        YOffsetLabel = QLabel("Y offset")
        YOffsetEntry = QSpinBox()
        YOffsetEntry.setMinimum(0)
        YOffsetEntry.setMaximum(1080 - 1)
        YOffsetEntry.setValue(svars.capture_y_offset)
        YOffsetEntry.setToolTip("Vertical offset (in pixels) from the top edge of the screen")
        YOffsetEntry.valueChanged.connect(svars.setyOffset)

        ####
        # LAYOUT
        ####

        optionsLayout = QGridLayout()
        optionsLayout.addWidget(ScreenModeLabel, 0, 0)
        optionsLayout.addWidget(ScreenModeDropdown, 0, 1)
        optionsLayout.addWidget(FullscreenCheckbox, 1, 0)
        optionsLayout.addWidget(WidthLabel, 2, 0)
        optionsLayout.addWidget(WidthEntry, 2, 1)
        optionsLayout.addWidget(HeightLabel, 3, 0)
        optionsLayout.addWidget(HeightEntry, 3, 1)
        optionsLayout.addWidget(XOffsetLabel, 4, 0)
        optionsLayout.addWidget(XOffsetEntry, 4, 1)
        optionsLayout.addWidget(YOffsetLabel, 5, 0)
        optionsLayout.addWidget(YOffsetEntry, 5, 1)
        self.OptionsBox.setLayout(optionsLayout)

        tabLayout = QGridLayout()
        tabLayout.addWidget(ActiveCheckbox, 0, 0)
        tabLayout.addWidget(self.OptionsBox, 1, 0)

        self.setLayout(tabLayout)

    def activateScreenRecording(self, state):
        """
        Turn On/Off screen mirroring. Enables/Disables hte Screen Mirroring tab

        :param state:
        """
        if state == Qt.Checked:
            self.rgb_effects.gvars.setMode(self.rgb_effects, 'screen_mirroring')
            self.OptionsBox.setEnabled(True)
        else:
            self.rgb_effects.gvars.setMode(self.rgb_effects, 'off')
            self.OptionsBox.setEnabled(False)
