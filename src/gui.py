import collections as COL
import csv as CSV
import os as OS
import pathlib as PTH
import shutil as SHU
import sys as SYS

import PySide6.QtWidgets as QTW

from fetch import *

Modification = COL.namedtuple("Modification", ["voice_over", "portrait", "name"])

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
    layout.addWidget(QTW.QLabel("Remove"), 0, 4)
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
      voice_over = layout.itemAtPosition(row, 1).widget().currentText()
      values[layout.itemAtPosition(row, 0).widget().currentText()] = Modification(
       voice_over if voice_over != _keep_centinel else "",
       layout.itemAtPosition(row, 2).widget().value,
       layout.itemAtPosition(row, 3).widget().text())
    return values

class MainWidget(QTW.QWidget):

  def __init__(self):
    super().__init__()
    layout = QTW.QVBoxLayout()
    self.replacements = ReplacementsWidget()
    layout.addWidget(self.replacements)
    buttons_layout = QTW.QHBoxLayout()

    self.add_button = QTW.QPushButton()
    self.add_button.setText("Add replacement")
    self.add_button.clicked.connect(self.replacements.add_row)
    buttons_layout.addWidget(self.add_button)

    self.load_button = QTW.QPushButton()
    self.load_button.setText("Load")
    buttons_layout.addWidget(self.load_button)

    self.install_button = QTW.QPushButton()
    self.install_button.setText("Install")
    self.install_button.clicked.connect(self.install)
    buttons_layout.addWidget(self.install_button)

    layout.addLayout(buttons_layout)
    self.setLayout(layout)

  def install(self):
    print(self.replacements.get_values())

_title = "Commander Aesthetic Replacer"

with open("commanders.csv") as csv:
  _unique_commanders = {row[0]: row[1:] for row in CSV.reader(csv)}

app = QTW.QApplication(SYS.argv)

_wows_folder = PTH.Path(
 QTW.QFileDialog.getExistingDirectory(None, "Choose WoWs folder"))
_working_folder = PTH.Path("working")
_output_folder = PTH.Path("res_mods")
for _folder in [_working_folder, _output_folder]:
  if folder.exists():
    SHU.rmtree(_folder)
  OS.makedirs(_folder)

unpack(_wows_folder, _working_folder, "banks/OfficialMods/*")
unpack(_wows_folder, _working_folder, "gui/crew_commander/base/*")

_keep_centinel = "(None)"
_voice_overs = [_keep_centinel] + fetch_voice_overs(_working_folder)

window = MainWidget()
window.show()

app.exec()
