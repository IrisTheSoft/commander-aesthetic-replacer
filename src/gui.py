import csv as CSV
import pathlib as PTH
import sys as SYS

import PySide6.QtWidgets as QTW

from fetch import *

_working_folder = PTH.Path("working")
_title = "Commander Aesthetic Replacer"

with open("unique.csv") as csv:
  unique_commanders = {row[0]: row[1:] for row in CSV.reader(csv)}

voice_overs = ["(None)"] + fetch_voice_overs(_working_folder)
portraits = fetch_portraits(_working_folder)

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
    self.add_row()
    self.add_row()

  def add_row(self):
    layout = self.layout()
    index = layout.rowCount()
    unique = QTW.QComboBox()
    unique.addItems(unique_commanders.keys())
    voice_over = QTW.QComboBox()
    voice_over.addItems(voice_overs)
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

class MainWidget(QTW.QWidget):

  def __init__(self):
    super().__init__()
    layout = QTW.QVBoxLayout()
    self.replacements = ReplacementsWidget()
    layout.addWidget(self.replacements)
    self.add_button = QTW.QPushButton()
    self.add_button.setText("Add replacement")
    self.add_button.clicked.connect(self.replacements.add_row)
    layout.addWidget(self.add_button)
    self.setLayout(layout)

app = QTW.QApplication(SYS.argv)

window = MainWidget()
window.show()

app.exec()
