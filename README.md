# WoWs Commander Aesthetic Replacer

This is a mod generator that allows changing the aesthetic (voice, portrait and name) of unique commanders.

## Usage

The first thing you'll be asked is the WoWs folder. From the base `World_of_Warships` folder, it should be `bin/<SomeNumber>` (usually the highest number in `bin`). After that it will start unpacking the required files, which can take several seconds.

Then the main screen will appear. At the bottom you should change "language" to the one you use **in-game**. You can also set the voice over mod name, but that's not very important.

Moving on to the table, first you must choose the unique commander that you want to tweak. In voice over there'll be an option for each voice over in the game. If you don't want to apply any, leave it as "(None)". In portrait you can choose any image from your computer, including of course the ones the game uses for other commanders. Note that this will only change the photo in port, not the armory one. You can click "Select" and then "Cancel" to blank that field and thus conserve the original portrait. If you leave blank the name field, the name won't be changed. You can also add more rows with the "Add" button at the top right corner and remove unused ones with their corresponding "Remove" button.

Once you're ready, press the "Install" button and wait until a "Success" message appears below. Then, exit the program and move the generated folder `<ModFolder>/res_mods` to the WoWs folder.

If you made any voice changes, you also need to choose your custom voice over from settings inside the game.

## Adding support for more commanders

So far, I've only tested these commanders:

* Yamamoto Isoroku.
* William F. Halsey Jr.
* Andrew Cunningham.
* Nikolay Kuznetsov.
* Günther Lütjens.
* Luigi Sansonetti.

In order to add support for another one, you'll have to find out 4 values (in order to support custom voice over, portrait and name, respectively):

* Any name that helps you identify it in the GUI.
* His `CrewName` for voice over. It could be just his surname with the first letter capitalized, but if it's not, I don't have much clue.
* His portrait file. While the program is at the main screen, you can browse `<ModFolder>/working/gui/crew_commander/base/` to find his portrait.
* His translation ID. You can search it in `<WowsFolder>/res/texts/en/LC_MESSAGES/global.mo`. It might be useful to convert it to `.po` for this purpose.

Once you have the values, put them separated by commas in a new row in `<ModFolder>/commanders.csv` with any text editor. You can also use that file to see examples of correct values.
