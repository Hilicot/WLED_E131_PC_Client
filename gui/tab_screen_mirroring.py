from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QRadioButton, QComboBox, \
    QColorDialog, QPushButton, QStyleFactory, QGroupBox, QSpinBox, QSlider, QCheckBox, QApplication
from PyQt5.QtCore import Qt

from screeninfo import get_monitors
from .GUI_variables import ScreenVariables


class TabScreen(QWidget):
    topLeftGroupBox = None
    topRightGroupBox = None
    bottomGroupBox = None

    ColorPickerBtn = None

    def __init__(self, parent, rgb_effects):
        super(TabScreen, self).__init__(parent)
        self.parent = parent
        self.rgb_effects = rgb_effects
        svars: ScreenVariables = rgb_effects.gvars.svars

        ####
        # WIDGETS
        ####

        self.ActiveCheckbox = QCheckBox("Screen Mirroring")
        self.ActiveCheckbox.stateChanged.connect(self.activateScreenRecording)

        self.OptionsBox = QGroupBox()

        ScreenModeLabel = QLabel("Mode")
        ScreenModeDropdown = QComboBox()
        ScreenModeDropdown.addItems(["Average", "Squared Average", "Fast"])
        ScreenModeDropdown.setCurrentText('Average')
        ScreenModeDropdown.currentIndexChanged.connect(svars.setScreenMode)

        SaturationBoostLabel = QLabel("Saturation Boost")
        SaturationBoostEntry = QSpinBox()
        SaturationBoostEntry.setMinimum(-255)
        SaturationBoostEntry.setMaximum(255)
        SaturationBoostEntry.setValue(svars.saturation_boost)
        SaturationBoostEntry.setToolTip("increase/decrease the saturation")
        SaturationBoostEntry.valueChanged.connect(svars.setSaturationBoost)
        FullscreenCheckbox = QCheckBox("Fullscreen")
        FullscreenCheckbox.stateChanged.connect(svars.setFullScreen)

        screen = get_monitors()[0]

        WidthLabel = QLabel("Width")
        WidthEntry = QSpinBox()
        WidthEntry.setMinimum(1)
        WidthEntry.setMaximum(screen.width)
        WidthEntry.setValue(svars.capture_width)
        WidthEntry.setToolTip("Insert the width (in pixels) of the capture area")
        WidthEntry.valueChanged.connect(svars.setWidth)
        HeightLabel = QLabel("Height")
        HeightEntry = QSpinBox()
        HeightEntry.setMinimum(1)
        HeightEntry.setMaximum(screen.height)
        HeightEntry.setValue(svars.capture_width)
        HeightEntry.setToolTip("Insert the height (in pixels) of the capture area")
        HeightEntry.valueChanged.connect(svars.setHeight)
        XOffsetLabel = QLabel("X offset")
        XOffsetEntry = QSpinBox()
        XOffsetEntry.setMinimum(0)
        XOffsetEntry.setMaximum(screen.width - 1)
        XOffsetEntry.setValue(svars.capture_x_offset)
        XOffsetEntry.setToolTip("Horizontal offset (in pixels) from the left edge of the screen")
        XOffsetEntry.valueChanged.connect(svars.setXOffset)
        YOffsetLabel = QLabel("Y offset")
        YOffsetEntry = QSpinBox()
        YOffsetEntry.setMinimum(0)
        YOffsetEntry.setMaximum(screen.height - 1)
        YOffsetEntry.setValue(svars.capture_y_offset)
        YOffsetEntry.setToolTip("Vertical offset (in pixels) from the top edge of the screen")
        YOffsetEntry.valueChanged.connect(svars.setyOffset)

        ####
        # LAYOUT
        ####

        optionsLayout = QGridLayout()
        optionsLayout.addWidget(ScreenModeLabel, 0, 0)
        optionsLayout.addWidget(ScreenModeDropdown, 0, 1)
        optionsLayout.addWidget(SaturationBoostLabel, 1, 0)
        optionsLayout.addWidget(SaturationBoostEntry, 1, 1)
        optionsLayout.addWidget(FullscreenCheckbox, 2, 0)
        optionsLayout.addWidget(WidthLabel, 3, 0)
        optionsLayout.addWidget(WidthEntry, 3, 1)
        optionsLayout.addWidget(HeightLabel, 4, 0)
        optionsLayout.addWidget(HeightEntry, 4, 1)
        optionsLayout.addWidget(XOffsetLabel, 5, 0)
        optionsLayout.addWidget(XOffsetEntry, 5, 1)
        optionsLayout.addWidget(YOffsetLabel, 6, 0)
        optionsLayout.addWidget(YOffsetEntry, 6, 1)
        self.OptionsBox.setLayout(optionsLayout)

        tabLayout = QGridLayout()
        tabLayout.addWidget(self.ActiveCheckbox, 0, 0)
        tabLayout.addWidget(self.OptionsBox, 1, 0)

        self.setLayout(tabLayout)

    def activateScreenRecording(self, state):
        """
        Turn On/Off screen mirroring. Enables/Disables hte Screen Mirroring tab

        :param state:
        """
        registered_mode = self.rgb_effects.gvars.mode
        if registered_mode not in ('screen_mirroring','off'):
            mode = registered_mode
        else:
            mode = 'screen_mirroring' if state else 'off'

        # set the mode
        self.rgb_effects.gvars.setMode(self.rgb_effects, mode)

        # (GUI) check the appropriate radio button in the general tab
        for i, radio in enumerate(self.parent.tab_general.RGBSelectionRadio):
            if radio[1] == mode:
                radio[0].setChecked(True)
                break

        # (GUI) enable/disable this tab
        self.OptionsBox.setEnabled(state)

    def enableUI(self, state):
        self.OptionsBox.setEnabled(state)
        self.ActiveCheckbox.blockSignals(True) # prevent triggering activateScreenRecording(state)
        self.ActiveCheckbox.setChecked(state)
        self.ActiveCheckbox.blockSignals(False)
