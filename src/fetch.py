import xml.etree.ElementTree as ET

voice_over_xpath = "./AudioModification/ExternalEvent/Container/Path/StateList/State[Name='CrewName']/Value"

def fetch_voice_overs(working_folder):
  voice_overs = set()
  for file_name in (working_folder/"banks"/"OfficialMods").glob("*/mod.xml"):
    tree = ET.parse(file_name)
    voice_overs.update(node.text for node in tree.findall(voice_over_xpath))
  voice_overs = list(voice_overs)
  voice_overs.sort()
  return voice_overs

def fetch_portraits(working_folder):
  return (working_folder/"gui"/"crew_commander"/"base").glob("*/*.png")
