from abjad import *
import copy


def test_NamedPitch___copy___01( ):

   pitch = pitchtools.NamedChromaticPitch(13)
   new = copy.copy(pitch)

   assert new is not pitch
   assert new.accidental is not pitch.accidental
