from abjad import *


def test_HarmonicChromaticIntervalClass___init__01( ):
   
   hcic = pitchtools.HarmonicChromaticIntervalClass(0)
   assert repr(hcic) == 'HarmonicChromaticIntervalClass(0)'
   assert str(hcic) == '0'
   assert hcic.number == 0

   hcic = pitchtools.HarmonicChromaticIntervalClass(12)
   assert hcic.number == 12

   hcic = pitchtools.HarmonicChromaticIntervalClass(24)
   assert hcic.number == 12

   hcic = pitchtools.HarmonicChromaticIntervalClass(-12)
   assert hcic.number == 12

   hcic = pitchtools.HarmonicChromaticIntervalClass(-24)
   assert hcic.number == 12


def test_HarmonicChromaticIntervalClass___init___02( ):

   hcic = pitchtools.HarmonicChromaticIntervalClass(-25)
   assert hcic.number == 1

   hcic = pitchtools.HarmonicChromaticIntervalClass(-13)
   assert hcic.number == 1

   hcic = pitchtools.HarmonicChromaticIntervalClass(-1)
   assert hcic.number == 1

   hcic = pitchtools.HarmonicChromaticIntervalClass(1)
   assert hcic.number == 1

   hcic = pitchtools.HarmonicChromaticIntervalClass(13)
   assert hcic.number == 1

   hcic = pitchtools.HarmonicChromaticIntervalClass(25)
   assert hcic.number == 1
