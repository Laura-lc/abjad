from abjad import *
from abjad.tools import tonalitytools


def test_SuspensionIndicator__init_by_start_and_stop_01( ):

   t = tonalitytools.SuspensionIndicator(4, 3)

   assert t.start == tonalitytools.ScaleDegree(4)
   assert t.stop == tonalitytools.ScaleDegree(3)


def test_SuspensionIndicator__init_by_start_and_stop_02( ):

   t = tonalitytools.SuspensionIndicator(4, ('flat', 3))

   assert t.start == tonalitytools.ScaleDegree(4)
   assert t.stop == tonalitytools.ScaleDegree('flat', 3)
