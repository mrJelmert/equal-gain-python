import os
import xml.etree.cElementTree as ET

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from decide import decide_base_path


class SettingsFormWidget(QtWidgets.QFormLayout):
    """
    FormLayout containing the different parameters for the model
    """

    def __init__(self, settings, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = settings
        self.main_window = main_window

        self.fixed_weight = QtWidgets.QDoubleSpinBox()
        self.fixed_weight.setSingleStep(0.05)
        self.fixed_weight.setDecimals(2)
        self.fixed_weight.setValue(0.10)
        self.fixed_weight.setMaximum(1)

        self.salience_weight = QtWidgets.QDoubleSpinBox()
        self.salience_weight.setSingleStep(0.05)
        self.salience_weight.setMaximum(1)
        self.salience_weight.setDecimals(2)
        self.salience_weight.setValue(0.40)

        self.randomized_value = QtWidgets.QDoubleSpinBox()
        self.randomized_value.setSingleStep(0.05)

        self.start = QtWidgets.QDoubleSpinBox()
        self.start.setSingleStep(0.05)
        self.start.valueChanged.connect(self.state_changed)

        self.step = QtWidgets.QDoubleSpinBox()
        self.step.setSingleStep(0.05)
        self.step.valueChanged.connect(self.state_changed)

        self.stop = QtWidgets.QDoubleSpinBox()
        self.stop.setSingleStep(0.05)
        self.stop.valueChanged.connect(self.state_changed)

        self.iterations = QtWidgets.QSpinBox()
        self.iterations.setMinimum(1)
        self.iterations.setValue(10)
        self.iterations.setMaximum(10000)

        self.repetitions = QtWidgets.QSpinBox()
        self.repetitions.setMinimum(1)
        self.repetitions.setValue(10)
        self.repetitions.setMaximum(10000)

        self.addRow(QtWidgets.QLabel("Fixed weight"), self.fixed_weight)
        self.addRow(QtWidgets.QLabel("Salience weight"), self.salience_weight)
        self.addRow(QtWidgets.QLabel(""))
        self.addRow(QtWidgets.QLabel("Negotiation rounds"), self.iterations)
        self.addRow(QtWidgets.QLabel("Simulation repetitions"), self.repetitions)
        self.addRow(QtWidgets.QLabel(""))

        self.addRow(QtWidgets.QLabel("p-value"))
        self.addRow(QtWidgets.QLabel("Start"), self.start)
        self.addRow(QtWidgets.QLabel("Step"), self.step)
        self.addRow(QtWidgets.QLabel("Stop"), self.stop)

    def load(self):
        """
        Copy the values from the ProgramSettings object
        """

        settings = self.settings.__dict__.items()

        for key, value in settings:
            if hasattr(self, key):
                attr = getattr(self, key)

                if isinstance(value, bool):  # type: QtWidgets.QAction
                    attr.setChecked(value)
                if isinstance(attr, list):
                    self.settings.__dict__[attr] = value
                else:
                    attr.setValue(value)

    def save(self):
        """
        Set the attributes to the ProgramSettings object
        """
        settings = self.__dict__.items()

        for key, value in settings:
            if hasattr(self.settings, key):
                setattr(self.settings, key, value.value())

    def state_changed(self):
        self.main_window.overview_widget.update_widget()


class ProgramSettings(QtCore.QObject):
    """
    The settings for the model parameters
    """

    changed = QtCore.pyqtSignal()

    settings_file = os.path.join(decide_base_path, "decide-settings.xml")

    def __init__(self, *args, **kwargs):
        super(ProgramSettings, self).__init__(*args, **kwargs)

        self.input_filename = ""
        self.output_directory = ""

        self.salience_weight = 0.4
        self.fixed_weight = 0.1

        self.randomized_value = 0.00
        self.start = 0.00
        self.step = 0.05
        self.stop = 0.50

        self.repetitions = 10
        self.iterations = 10

        self.settings_type = "xml"
        self.settings_list_separator = ";"

        self.version = 1

        self.output_sqlite = False
        self.issue_development_csv = True
        self.externalities_csv = False
        self.exchanges_csv = False
        self.voting_positions = False
        self.summary_only = True

        self.selected_actors = []
        self.selected_issues = []

    def settings_file_path(self):
        file_path = os.path.join(decide_base_path, self.settings_file)

        return file_path

    def save(self):
        if self.settings_type == "xml":
            self._save_xml()

    def _save_xml(self):

        file_path = self.settings_file_path()

        element = ET.Element("decide-settings")

        for key, value in self.__dict__.items():
            if not key.startswith("_") and hasattr(self, key):

                if isinstance(value, list):
                    value = self.settings_list_separator.join(value)

                child = ET.Element(key)
                child.text = str(value)
                element.append(child)

        ET.ElementTree(element).write(file_path)

    def load(self):
        if self.settings_type == "xml":
            self._load_xml()

    def _load_xml(self):

        file_path = os.path.join(decide_base_path, self.settings_file)

        if not os.path.exists(file_path):
            return

        for elm in ET.parse(file_path).getroot():

            if hasattr(self, elm.tag):

                attr = getattr(self, elm.tag)

                if isinstance(attr, bool):
                    setattr(self, elm.tag, elm.text == "True")
                elif isinstance(attr, int):
                    setattr(self, elm.tag, int(elm.text))
                elif isinstance(attr, float):
                    setattr(self, elm.tag, float(elm.text))
                elif isinstance(attr, list):
                    setattr(
                        self, elm.tag, str(elm.text).split(self.settings_list_separator)
                    )
                else:
                    setattr(self, elm.tag, str(elm.text))
