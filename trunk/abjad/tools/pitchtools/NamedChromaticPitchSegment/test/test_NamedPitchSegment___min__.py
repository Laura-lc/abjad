from abjad import *


def test_NamedPitchSegment___min___01( ):

   pitch_segment = pitchtools.NamedChromaticPitchSegment([-2, -1.5, 6, 7, -1.5, 7])
   assert min(pitch_segment) == pitchtools.NamedChromaticPitch(-2)
