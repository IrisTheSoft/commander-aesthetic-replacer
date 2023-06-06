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
    path = QTW.QFileDialog.getOpenFileName(self, "Open file",
     str(_working_folder/"gui"/"crew_commander"/"base"))[0]
    self.label.setText(path)

class ReplacementWidget(QTW.QWidget):

  def __init__(self):
    super().__init__()
    layout = QTW.QFormLayout()

    self.uniques = QTW.QComboBox()
    self.uniques.addItems(unique_commanders)
    layout.addRow("Commander:", self.uniques)

    self.voice_overs = QTW.QComboBox()
    self.voice_overs.addItems(voice_overs)
    layout.addRow("Voice over:", self.voice_overs)

    self.portraits = FileSelector()
    layout.addRow("Portrait:", self.portraits)

    self.names = QTW.QLineEdit()
    layout.addRow("Name:", self.names)

    self.setLayout(layout)

  def choose_portrait(self):
    path = QTW.QFileDialog.getOpenFileName(self, "Open file")[0]
    self.portraits.setText(path)

class MainWindow(QTW.QMainWindow):

  def __init__(self):
    super().__init__()
    self.setWindowTitle(_title)
    self.setCentralWidget(ReplacementWidget())

app = QTW.QApplication(SYS.argv)

window = MainWindow()
window.show()

app.exec()
