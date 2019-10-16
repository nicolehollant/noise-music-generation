import numpy as np
from midiutil import MIDIFile
import random
import json

all_chords = json.load(open("music/conf/chords.json", "r"))
base_key = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
permitted_chords = [
  'C', 'C7', 'C9', 'C11', 'CM7', 'CM9', 'CM11',
  'Dm9', 'Dm', 'Dm6', 'Dm7', 
  'Em9', 'Em', 'Em6', 'Em7', 
  'F', 'F7', 'F9', 'F11', 'FM7', 'FM9', 'FM11', 
  'G', 'G7', 'G9', 'G11', 'GM7', 'GM9', 'GM11', 
  'Am9', 'Am', 'Am6', 'Am7',
]

base_chords = []
for x in base_key:
  for key, val in all_chords[x].items():
    if key in permitted_chords:
      base_chords.append(val)