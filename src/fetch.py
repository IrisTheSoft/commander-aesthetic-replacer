import os as OS
import subprocess as SPROC
import xml.etree.ElementTree as ET

_voice_over_xpath = "./AudioModification/ExternalEvent/Container/Path/StateList/State[Name='CrewName']/Value"

def fetch_voice_overs(working_folder):
  voice_overs = set()
  for file_name in (working_folder/"banks"/"OfficialMods").glob("*/mod.xml"):
    tree = ET.parse(file_name)
    voice_overs.update(node.text for node in tree.findall(_voice_over_xpath))
  voice_overs = list(voice_overs)
  voice_overs.sort()
  return voice_overs

def fetch_portraits(working_folder):
  base_path = working_folder/"gui"/"crew_commander"/"base"
  portraits = {}
  for path in base_path.glob("*/*.png"):
    nation = path.parent.name
    if nation not in portraits:
      portraits[nation] = []
    portraits[nation].append(path.stem)
  for portrait_list in portraits.values():
    portrait_list.sort()
  return portraits

def fetch_languages(wows_folder):
  return OS.listdir(wows_folder/"res/texts")

def unpack(wows_folder, working_folder, pattern):
  SPROC.run(["wowsunpack.exe",
   "-x", wows_folder/"idx",
   "-p", "../../../res_packages",
   "-I", pattern,
   "-o", working_folder],
   check=True)
