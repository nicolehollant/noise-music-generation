import pprint
import json

c_chords = {}
chords = {}
base_8 = "1 #1 2 #2 3 4 #4 5 #5 6 #6 7 8 #8 9 #9 10 11".split(' ')
base_12 = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18".split(' ')

def is_sharp(x):
  return int(x) % 13 in [2, 4, 7, 9, 11]

def to_base8(x):
  ind = base_12.index(str((int(x) % 12) + 1))
  return base_8[ind]

notes = "C C# D D# E F F# G G# A A# B".split(' ')

with open('c_chords', 'r') as f:
  for line in f.readlines():
    sections = line.split('--')
    c_chords[sections[0]] = [x.strip() for x in sections[1].split(' ')]

for i, note in enumerate(notes):
  current = {}
  for key, val in c_chords.items():
    new_key = key.replace('C', note)
    new_val = []
    for x in val:
      new_val.append(((int(x) + i - 1) % 12) + 24)
    current[new_key] = new_val
  chords[note] = current

with open("chords.json", "w") as f:
  json.dump(chords, f, indent=2)