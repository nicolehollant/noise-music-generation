from music.tunes import Instrument, Guitar, NoArp, Rhythm, Lead
import math
import random

class Song():
  """
  [Question Two]
  - Recreate data for Figure 15.17 (guestimate what the data is), 
    calculate the coefficient of variance and plot it for each region
  """
  def __init__(self, outdir="tmp", bpm=100, minutes=3.5, key='c', instruments=None):
    self.noise_offset = (random.random() - 0.5) * 2
    self.outdir = outdir
    self.bpm = bpm
    self.beats = math.ceil(minutes * bpm)
    self.key = key
    self.instruments = instruments
    if not self.instruments:
      self.instruments = {
        'guitar': { 
          'instrument': 'guitar',
          'outfile': 'guitar',
          'one_handed': True,
          'p_chord': 0.2,
          'octave_range': [2, 4]
        },
        'bass': { 
          'instrument': 'instrument',
          'outfile': 'bass',
          'one_handed': True,
          'p_chord': 0.01,
          'octave_range': [0, 3]
        },
        'drums': { 
          'instrument': 'instrument',
          'outfile': 'drums',
          'p_chord': 0.3,
          'octave_range': [1, 3]
        },
        'violin': { 
          'instrument': 'instrument',
          'outfile': 'violin',
          'p_chord': 0.05,
          'one_handed': True,
          'octave_range': [3, 6]
        },
        'piano': { 
          'instrument': 'instrument',
          'outfile': 'piano',
          'p_chord': 0.1,
          'octave_range': [2, 6]
        },
        'piano_no_arp': { 
          'instrument': 'noarp',
          'outfile': 'piano_no_arp',
          'p_chord': 0.1,
          'octave_range': [2, 6]
        },
        'rhythm': { 
          'instrument': 'rhythm',
          'outfile': 'rhythm',
          'p_chord': 0.1,
          'octave_range': [2, 4]
        },
        'lead': { 
          'instrument': 'lead',
          'outfile': 'lead',
          'p_chord': 0.1,
          'octave_range': [2, 5]
        },
        'bass_lead': { 
          'instrument': 'lead',
          'outfile': 'bass_lead',
          'p_chord': 0.01,
          'one_handed': True,
          'octave_range': [0, 3]
        }
      }


  def make_tunes(self):
    """
    Run all problems!
    """
    for key, val in self.instruments.items():
      outfile = self.outdir + "/" + val.get('outfile', key)
      octave_range = val.get('octave_range', None)
      one_handed = val.get('one_handed', False)
      p_chord = val.get('p_chord', None)
      if val['instrument'] == 'lead':
        Lead(beats=self.beats, key=self.key, octave_range=octave_range, p_chord=p_chord, outfile=outfile, one_handed=one_handed, noise_offset=self.noise_offset).make_section(0, self.beats)
      elif val['instrument'] == 'guitar':
        Guitar(beats=self.beats, key=self.key, octave_range=octave_range, p_chord=p_chord, outfile=outfile, one_handed=one_handed, noise_offset=self.noise_offset).make_section(0, self.beats)
      elif val['instrument'] == 'noarp':
        NoArp(beats=self.beats, key=self.key, octave_range=octave_range, p_chord=p_chord, outfile=outfile, one_handed=one_handed, noise_offset=self.noise_offset).make_song()
      elif val['instrument'] == 'rhythm':
        Rhythm(beats=self.beats, key=self.key, octave_range=octave_range, p_chord=p_chord, outfile=outfile, one_handed=one_handed, noise_offset=self.noise_offset).make_section(0, self.beats)
      elif val['instrument'] == 'instrument':
        Instrument(beats=self.beats, key=self.key, octave_range=octave_range, p_chord=p_chord, outfile=outfile, one_handed=one_handed, noise_offset=self.noise_offset).make_song()