import collections as COL
import csv as CSV
import os as OS
import pathlib as PTH
import shutil as SHU
import sys as SYS

import PySide6.QtWidgets as QTW

from fetch import *
from install import *

Modification = COL.namedtuple("Modification", ["voice_over", "portrait", "name"])
Commander = COL.namedtuple("Commander", ["voice_over", "portrait", "name_id"])

class FileSelector(QTW.QWidget):

  def __init__(self):
    super().__init__()
    self.value = ""

    layout = QTW.QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)

    self.button = QTW.QPushButton()
    self.button.setText("Select")
    self.button.clicked.connect(self.update_label)
    layout.addWidget(self.button)

    self.label = QTW.QLabel()
    layout.addWidget(self.label)

    self.setLayout(layout)

  def update_label(self):
    self.value = QTW.QFileDialog.getOpenFileName(self, "Open file",
     str(_working_folder/"gui"/"crew_commander"/"base"))[0]
    self.label.setText("/".join(self.value.rsplit("/", 2)[1:]))

class ReplacementsWidget(QTW.QWidget):

  def __init__(self):
    super().__init__()
    layout = QTW.QGridLayout()
    layout.addWidget(QTW.QLabel("Commander"), 0, 0)
    layout.addWidget(QTW.QLabel("Voice over"), 0, 1)
    layout.addWidget(QTW.QLabel("Portrait"), 0, 2)
    layout.addWidget(QTW.QLabel("Name"), 0, 3)

    self.add_button = QTW.QPushButton()
    self.add_button.setText("Add")
    self.add_button.clicked.connect(self.add_row)
    layout.addWidget(self.add_button, 0, 4)
    self.setLayout(layout)
    self.add_row()

  def add_row(self):
    layout = self.layout()
    index = layout.rowCount()
    unique = QTW.QComboBox()
    unique.addItems(_unique_commanders.keys())
    voice_over = QTW.QComboBox()
    voice_over.addItems(_voice_overs)
    portrait = FileSelector()
    name = QTW.QLineEdit()
    remove = QTW.QPushButton()
    remove.setText("Remove")
    remove.clicked.connect(lambda: self.remove_row(unique))
    layout.addWidget(unique, index, 0)
    layout.addWidget(voice_over, index, 1)
    layout.addWidget(portrait, index, 2)
    layout.addWidget(name, index, 3)
    layout.addWidget(remove, index, 4)

  def remove_row(self, unique):
    layout = self.layout()
    index = layout.indexOf(unique)
    for _ in range(5):
      layout.takeAt(index).widget().setParent(None)

  def get_values(self):
    values = {}
    layout = self.layout()
    for row in range(1, layout.rowCount()):
      if layout.itemAtPosition(row, 1) is None:
        continue
      voice_over = layout.itemAtPosition(row, 1).widget().currentText()
      values[layout.itemAtPosition(row, 0).widget().currentText()] = Modification(
       voice_over if voice_over != _keep_centinel else "",
       layout.itemAtPosition(row, 2).widget().value,
       layout.itemAtPosition(row, 3).widget().text())
    return values

class MainWidget(QTW.QWidget):

  def __init__(self):
    super().__init__()
    self.setWindowTitle(_title)
    layout = QTW.QVBoxLayout()
    self.replacements = ReplacementsWidget()
    layout.addWidget(self.replacements)
    form_layout = QTW.QFormLayout()

    self.language_box = QTW.QComboBox()
    self.language_box.addItems(fetch_languages(_wows_folder))
    form_layout.addRow("Names Mod Language", self.language_box)
    self.voice_mod_name_box = QTW.QLineEdit("My Voice Mod")
    form_layout.addRow("Voice Mod Name", self.voice_mod_name_box)

    self.install_button = QTW.QPushButton()
    self.install_button.setText("Install")
    self.install_button.clicked.connect(self.install)
    form_layout.addWidget(self.install_button)

    layout.addLayout(form_layout)
    self.setLayout(layout)

  def install(self):
    self.install_button.setDisabled(True)

    voice_over_changes = {}
    portrait_changes = {}
    name_changes = {}

    for commander_name, modification in self.replacements.get_values().items():
      commander = _unique_commanders[commander_name]
      if modification.voice_over != "":
        if modification.voice_over not in voice_over_changes.keys():
          voice_over_changes[modification.voice_over] = []
        voice_over_changes[modification.voice_over].append(commander.voice_over)
      if modification.portrait != "":
        portrait_changes[commander.portrait] = modification.portrait
      if modification.name != "":
        name_changes[commander.name_id] = modification.name

    install_voice_overs(_working_folder, _output_folder,
      _title.replace(" ", ""), self.voice_mod_name_box.text(), voice_over_changes)
    install_portraits(_working_folder, _output_folder, portrait_changes)
    install_names(_wows_folder, _output_folder, self.language_box.currentText(),
      name_changes)

    SHU.rmtree(_working_folder)

    self.layout().addWidget(QTW.QLabel("Success!"))

_title = "Commander Aesthetic Replacer"

with open("commanders.csv") as csv:
  _unique_commanders = {row[0]: Commander(*row[1:]) for row in CSV.reader(csv)}

app = QTW.QApplication(SYS.argv)

_wows_folder = PTH.Path(
 QTW.QFileDialog.getExistingDirectory(None, "Choose WoWs folder"))
_working_folder = PTH.Path("working")
_output_folder = PTH.Path("res_mods")
for _folder in [_working_folder, _output_folder]:
  if _folder.exists():
    SHU.rmtree(_folder)
  OS.makedirs(_folder)

unpack(_wows_folder, _working_folder, "banks/OfficialMods/*")
unpack(_wows_folder, _working_folder, "gui/crew_commander/base/*")

_keep_centinel = "(None)"
_voice_overs = [_keep_centinel] + fetch_voice_overs(_working_folder)

window = MainWidget()
window.show()

app.exec()
