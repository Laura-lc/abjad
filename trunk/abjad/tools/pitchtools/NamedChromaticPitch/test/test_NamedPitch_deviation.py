from abjad import *


def test_NamedPitch_deviation_01( ):
   '''Deviation defaults to None.'''

   p = pitchtools.NamedChromaticPitch('bf', 4)
   assert p.deviation is None


def test_NamedPitch_deviation_02( ):
   '''Deviation can be int or float.'''

   #p = pitchtools.NamedChromaticPitch('bf', 4)

   #p.deviation = -31
   p = pitchtools.NamedChromaticPitch('bf', 4, -31)
   assert p.deviation == -31

   #p.deviation = -12.4
   p = pitchtools.NamedChromaticPitch('bf', 4, -12.4)
   assert p.deviation == -12.4
