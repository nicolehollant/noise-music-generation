import math
from music.conf import MIDIFile, random, base_chords
from music.tunes.Note import Note

class Instrument:

  def __init__(self, track=0, channel=0, tempo=200, beats=200, key='c', outfile='test', octave_range=None, p_chord=None, one_handed=None, noise_offset=0):
    self.midi = MIDIFile(1)
    self.midi.addTempo(track, 0, tempo)
    self.midi.addTempo(track, 1, tempo)
    self.beats = beats
    self.track = track
    self.noise_offset = noise_offset
    self.outfile = outfile
    self.p_chord = p_chord
    self.one_handed = one_handed
    if not p_chord:
      self.p_chord = 0.3
    if not one_handed:
      self.one_handed = False
    if not octave_range:
      self.octave_range = [2,5]
    self.note = Note(key=key, octave_range=octave_range)
    self.is_playing_chord = False
    self.is_playing_arp = False
    self.chord_done = 0
    self.beat = 0
  
  def make_song(self, p_nothing=0.6):
    for i in range(self.beats - 100):
      if i > self.chord_done:
        self.is_playing_chord = False
        self.is_playing_arp = False
      volume = random.randrange(70, 100)
      duration = random.randrange(1, 16)
      randchoice = random.random()
      if randchoice <= self.p_chord and not (self.one_handed and self.is_playing_chord):
        self.is_playing_chord = True
        self.chord_done = i + duration
        chord = self.note.make_chord()
        if random.random() < 0.7:
          duration = random.randrange(2, 6)
          self.chord_done = i + duration
          self.is_playing_arp = True
          for j, note in enumerate(chord):
            d = j*duration/len(chord)
            self.midi.addNote(self.track, 1, note, i + d, 2, volume + random.randrange(-20, 20))
        else:
          for note in chord:
            self.midi.addNote(self.track, 0, note, i, duration, volume + random.randrange(-20, 20))
      elif randchoice <= p_nothing:
        self.midi.addNote(self.track, 0, self.note.make_note(), i, duration, volume)
    self.writeMidi()

  @staticmethod
  def write_chords():
    with open(f"out/chords.mid", "wb") as output_file:
      m = Instrument(beats=1000, key='c', octave_range=[3, 6])
      common_chords = [
        [0, 2, 4],
        [1, 3, 5],
        [2, 4, 6],
        [4, 6, 1],
        [5, 0, 2],
        [6, 1, 3],
      ]
      base_scale = [24, 26, 28, 29, 31, 33, 35]
      for i, chord in enumerate(common_chords):
        for note in chord:
          m.midi.addNote(m.track, 0, base_scale[note] + 36, i, 1, 100)
      m.midi.writeFile(output_file)
    
  def writeMidi(self):
    with open(f"out/{self.outfile}.mid", "wb") as output_file:
      self.midi.writeFile(output_file)

class Guitar(Instrument):

  def add_note(self, note, time, duration, volume=random.randint(85, 100), channel=0):
    self.midi.addNote(self.track, channel, note, time, duration, volume + random.randrange(-20, 20))

  def add_chord(self, chord, time, duration, volume=random.randint(85, 100), channel=1):
    for j, note in enumerate(chord):
      self.midi.addNote(self.track, j % 12, note % 127, time, duration, volume + random.randrange(-20, 20))
  
  def add_arpeggio(self, chord, time, duration, volume=random.randint(85, 100), channel=2):
    for j, note in enumerate(chord):
      d = j * duration / len(chord)
      print('note', note, 'dur', d)
      self.midi.addNote(self.track, j % 12, note % 127, time + d, duration / len(chord), volume + random.randrange(-20, 20))
  
  def add_notes(self, notes, time, volume=random.randint(85, 100), channel=2):
    d = 0
    j = 0
    for note, dur in notes:
      d += dur
      j+=1
      print(f"Note {note} dur {dur}")
      self.midi.addNote(self.track, j % 12, note % 127, time + d, dur, volume + random.randrange(-20, 20))

  def rand_duration(self, upper=4, lower=1, allow_partials=True):
    if allow_partials and random.random() < 0.5:
      return random.choice([0.25, 0.5, 0.75, 1])
    else:
      return random.randint(lower, upper)
    
  def motif(self, upper=16):
    num_parts = random.randint(8, upper)
    motif = []
    for i in range(num_parts):
      sound = self.make_sound(i, p_chord=0.1)
      upper = 4
      lower = 1
      if sound[1] == "arpeggio":
        upper = 8
        lower = 4
        motif.append([sound, self.rand_duration(upper=upper, lower=lower, allow_partials=False)])
      else:
        motif.append([sound, self.rand_duration(upper=upper, lower=lower)])
    return motif

  def make_chord(self):
    return self.note.make_chord()

  def make_arpeggio(self):
    chord = self.make_chord()
    chord.sort()
    r = random.random()
    if r < 0.3:
      random.shuffle(chord)
    elif r < 0.6:
      chord.reverse()
    return chord

  def chord_progression(self):
    num_chords = random.randint(2, 8)
    chords = []
    for _ in range(num_chords):
      chords.append([self.make_chord(), self.rand_duration(upper=8)])
    return chords

  def make_note(self, i, j):
    return self.note.make_note_noise(i, j, self.noise_offset)

  def make_notes(self, i):
    num_notes = random.randint(4, 16)
    notes = []
    for j in range(num_notes):
      notes.append([self.make_note(i, j), self.rand_duration(upper=2)])
    return notes

  def make_sound(self, i, p_chord=0.2, p_arp=0.2, p_single=0.2):
    r = random.random()
    if r < p_chord:
      return [self.make_chord(), 'chord']
    elif r < (p_chord + p_arp):
      return [self.make_arpeggio(), 'arpeggio']
    else:
      return [self.make_note(i, self.beat), 'note']

  def write_chord_progression(self, progression, cursor, i):
    curr_prog = progression[cursor]
    self.add_chord(curr_prog[0], i, curr_prog[1])
    self.done_blocking = i + curr_prog[1]
    cursor += 1
    if cursor >= len(progression):
      cursor = 0
    return cursor

  def write_notes(self, notes, cursor, i):
    self.add_notes(notes, i)
    self.done_blocking = i + math.ceil(sum([note[1] for note in notes]))
    return cursor

  def write_motif(self, motif, cursor, i):
    curr_sound = motif[cursor]
    if curr_sound[0][1] == 'chord':
      self.add_chord(curr_sound[0][0], i, curr_sound[1])
    elif curr_sound[0][1] == 'arpeggio':
      self.add_arpeggio(curr_sound[0][0], i, curr_sound[1])
    else:
      self.add_note(curr_sound[0][0], i, curr_sound[1])
    self.done_blocking = i + curr_sound[1]
    cursor += 1
    if cursor >= len(motif):
      cursor = 0
    return cursor

  def make_section(self, section_start, section_end):
    motif = self.motif()
    verse = self.motif(upper=40)
    progression = self.chord_progression()
    self.done_blocking = section_start
    motif_cursor = 0
    verse_cursor = 0
    chord_cursor = 0
    note_cursor = 0
    current_section = 0
    sections = ['chord', 'motif', 'verse', 'notes']
    for i in range(section_start, section_end-100):
      self.beat = i
      if i >= self.done_blocking:
        if sections[current_section] == 'chord':
          chord_cursor = self.write_chord_progression(progression, chord_cursor, i)
        elif sections[current_section] == 'motif':
          motif_cursor = self.write_motif(motif, motif_cursor, i)
        elif sections[current_section] == 'verse':
          verse_cursor = self.write_motif(verse, verse_cursor, i)
        else:
          note_cursor = self.write_notes(self.make_notes(i), note_cursor, i)
        current_section += 1
        if current_section >= len(sections):
          current_section = 0
    self.writeMidi()

class NoArp(Instrument):
  def make_song(self, p_nothing=0.6):
    for i in range(self.beats - 100):
      volume = random.randrange(70, 100)
      duration = random.randrange(1, 16)
      randchoice = random.random()
      if randchoice <= self.p_chord:
        for note in self.note.make_chord():
          self.midi.addNote(self.track, 0, note, i, duration, volume + random.randrange(-20, 20))
      elif randchoice <= p_nothing:
        self.midi.addNote(self.track, 0, self.note.make_note(), i, duration, volume)
    self.writeMidi()

class Rhythm(Guitar):
  def make_section(self, section_start, section_end):
    progression = self.chord_progression()
    progression2 = self.chord_progression()
    progression3 = self.chord_progression()
    self.done_blocking = section_start
    chord_cursor = 0
    chord2_cursor = 0
    chord3_cursor = 0
    current_section = 0
    sections = ['chord', 'chord2', 'chord', 'chord3']
    for i in range(section_start, section_end-100):
      if i >= self.done_blocking:
        if sections[current_section] == 'chord':
          chord_cursor = self.write_chord_progression(progression, chord_cursor, i)
        elif sections[current_section] == 'chord2':
          chord2_cursor = self.write_chord_progression(progression2, chord2_cursor, i)
        else:
          chord3_cursor = self.write_chord_progression(progression3, chord3_cursor, i)
        current_section += 1
        if current_section >= len(sections):
          current_section = 0
    self.writeMidi()

class Lead(Guitar):
  def make_section(self, section_start, section_end):
    motif = self.motif()
    verse = self.motif(upper=40)
    self.done_blocking = section_start
    motif_cursor = 0
    verse_cursor = 0
    note_cursor = 0
    current_section = 0
    sections = ['motif', 'verse', 'motif', 'notes']
    for i in range(section_start, section_end-100):
      if i >= self.done_blocking:
        if sections[current_section] == 'motif':
          motif_cursor = self.write_motif(motif, motif_cursor, i)
        elif sections[current_section] == 'verse':
          verse_cursor = self.write_motif(verse, verse_cursor, i)
        else:
          note_cursor = self.write_notes(self.make_notes(i), note_cursor, i)
        current_section += 1
        if current_section >= len(sections):
          current_section = 0
    self.writeMidi()