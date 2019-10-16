import math
from music.conf import MIDIFile, random, base_chords
import noise

class Note:

  def __init__(self, key='c', octave_range=[2,5]):
    self.key = key
    self.octaves = 6
    if any([x < 0 or x > 6 for x in octave_range]):
      raise ValueError('Octaves must be between 0 and 6')
    self.octave_range = range(octave_range[0], octave_range[1])
    base_scale = [24, 26, 28, 29, 31, 33, 35]
    self.keys = {"c": base_scale}
    for i, key in enumerate(["c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]):
      self.keys[key] = [x + i + 1 for x in self.keys["c"]]
    self.k = self.keys[self.key]
    self.common_chords = [
      [0, 2, 4],
      [1, 3, 5],
      [2, 4, 6],
      [4, 6, 1],
      [5, 0, 2],
      [6, 1, 3],
    ]
    self.all_notes = []
    for r in self.octave_range:
      self.all_notes.extend([note + (12 * r) for note in self.k])

  def make_chord(self, p_rand=0.1, n_notes=4, p_double=0.5):
    isdouble = False
    if random.random() < p_double:
      isdouble = True
      n_notes*=2
    if random.random() <= p_rand:
      return [self.make_note() for i in range(n_notes)]

    chord = random.choice(base_chords)
    octave = (random.choice(self.octave_range) * 12)
    if isdouble:
      double_octave = (random.choice(self.octave_range) * 12)
      while double_octave == octave:
        octave = (random.choice(self.octave_range) * 12)
      c = [note + double_octave for note in chord]
      c.extend([note + octave for note in chord])
      return c
    return [note + octave for note in chord]

  def make_note(self):
    octave = random.choice(self.octave_range) * 12
    return random.choice(self.k) + octave
  
  def make_note_noise(self, i, j, noise_offset):
    noises = noise.pnoise3(float(i)/len(self.all_notes), math.sin(float(j)), noise_offset)
    noise_1 = float(noises + 1) / 2
    print(f"noise1: {noise_1} {noise.pnoise1(i)} max: {len(self.all_notes)} i {i} j {j} offset {noise_offset}")
    ind = math.floor(noise_1 * len(self.all_notes))
    return self.all_notes[ind]