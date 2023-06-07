import copy as CP
import os as OS
import pathlib as PTH
import shutil as SHU
import xml.etree.ElementTree as ET

import polib as PO

_modified_centinel = "modified"
_wem_name_xpath = "./AudioModification/ExternalEvent/Container/Path/FilesList/File/Name"
_crew_name_xpath = ("./AudioModification/ExternalEvent/Container/Path/StateList/" +
 "State[Name='CrewName']/Value")
_modified_xpath = ("./AudioModification/ExternalEvent/Container/Path/StateList/" +
 "State[Name='CrewName']/Value[@modified]")
_path_relative_xpath = ("./Container/Path/StateList/State[Name='CrewName']/" +
 f"Value[@{_modified_centinel}]/../../..")
_crew_name_relative_xpath = "./StateList/State[Name='CrewName']/Value"

def install_voice_overs(working_folder, output_folder, mod_id, mod_name, changes):
  if not changes:
    return

  mod_folder = output_folder/"banks/Mods"/mod_id
  OS.makedirs(mod_folder)

  result_tree = ET.parse("voice-mod-template.xml")
  result_tree.find("./AudioModification/Name").text = mod_name

  for mod_file_name in PTH.Path(working_folder, "banks/OfficialMods").glob("*/mod.xml"):
    tree = ET.parse(mod_file_name)

    # Deal with duplicate file names in different folders
    for wem_name in tree.findall(_wem_name_xpath):
      wem_name.set("subfolder", mod_file_name.parent.name)
      wem_name.set("file_name", wem_name.text)
      wem_name.text = "{}___{}".format(
        wem_name.get("subfolder"), wem_name.get("file_name"))

    # Mark changes to crew names
    for crew_name in tree.findall(_crew_name_xpath):
      if crew_name.text in changes.keys():
        crew_name.set(_modified_centinel, _modified_centinel)

    # Merge into the result tree
    for external_event in tree.findall(_modified_xpath + "/.."*5):
      external_event_name = external_event.find("./Name").text
      result_external_event = result_tree.find(
        f"./AudioModification/ExternalEvent[Name='{external_event_name}']")
      if result_external_event is None:
        result_external_event = ET.SubElement(result_tree.find("./AudioModification"),
          "ExternalEvent")
        ET.SubElement(result_external_event, "Name").text = external_event_name
        container = ET.SubElement(result_external_event, "Container")
        ET.SubElement(container, "Name").text = "Voice"
        ET.SubElement(container, "ExternalId").text = "V" + external_event_name[5:]
      else:
        container = result_external_event.find("./Container")
      for path in external_event.findall(_path_relative_xpath):
        for target in changes[path.find(_crew_name_relative_xpath).text]:
          updated_path = CP.deepcopy(path)
          updated_path.find(_crew_name_relative_xpath).text = target
          container.append(updated_path)

  ET.indent(result_tree, space="  ", level=0)
  result_tree.write(mod_folder/"mod.xml", xml_declaration=True)

  required_wems = {(node.get("subfolder"), node.get("file_name"), node.text)
    for node in result_tree.findall(_wem_name_xpath)}
  for subfolder, old_file_name, new_file_name in required_wems:
    OS.rename(working_folder/"banks/OfficialMods"/subfolder/old_file_name,
      mod_folder/new_file_name)

def install_portraits(working_folder, output_folder, changes):
  if not changes:
    return

  mod_folder = output_folder/"gui/crew_commander/base"
  OS.makedirs(mod_folder)
  for destination, source in changes.items():
    full_destination = PTH.Path(mod_folder, destination)
    if not full_destination.parent.is_dir():
      OS.mkdir(full_destination.parent)
    SHU.copyfile(working_folder/"gui/crew_commander/base"/source, full_destination)

def install_names(wows_folder, output_folder, language, changes):
  if not changes:
    return

  mo = PO.mofile(wows_folder/"res/texts"/language/"LC_MESSAGES/global.mo")
  for entry in mo:
    if entry.msgid in changes:
      entry.msgstr = changes[entry.msgid]

  mod_folder = output_folder/"texts"/language/"LC_MESSAGES"
  OS.makedirs(mod_folder)
  mo.save(mod_folder/"global.mo")
