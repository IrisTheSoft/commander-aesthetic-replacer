import pathlib as PTH
import sys as SYS

import PySide6.QtWidgets as QTW

from fetch import *

_working_folder = PTH.Path("working")
_title = "Commander Aesthetic Replacer"

unique_commanders = {
  "Yamamoto Isoroku": None,
  "William F. Halsey Jr.": None,
  "Günther Lütjens": None,
  "Nikolay Kuznetsov": None,
  "Luigi Sansonetti": None,
  "Andrew Cunningham": None
}

voice_overs = ["(None)"] + fetch_voice_overs(_working_folder)
portraits = fetch_portraits(_working_folder)

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

    self.portraits_nations = QTW.QComboBox()
    self.portraits = QTW.QComboBox()
    self.portraits_nations.currentIndexChanged.connect(self.update_portraits)
    self.portraits_nations.addItems(sorted(portraits.keys()))
    layout.addRow("Portrait nation:", self.portraits_nations)
    layout.addRow("Portrait:", self.portraits)

    self.names = QTW.QLineEdit()
    layout.addRow("Name:", self.names)

    self.setLayout(layout)

  def update_portraits(self):
    self.portraits.clear()
    self.portraits.addItems(portraits[self.portraits_nations.currentText()])

class MainWindow(QTW.QMainWindow):

  def __init__(self):
    super().__init__()
    self.setWindowTitle(_title)
    self.setCentralWidget(ReplacementWidget())

app = QTW.QApplication(SYS.argv)

window = MainWindow()
window.show()

app.exec()
