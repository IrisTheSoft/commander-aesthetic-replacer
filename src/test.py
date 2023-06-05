import pathlib as PTH
from fetch import *

working_folder = PTH.Path("working")

print(*fetch_voice_overs(working_folder), sep="\n", end="\n\n")
print(*fetch_portraits(working_folder), sep="\n", end="\n\n")
