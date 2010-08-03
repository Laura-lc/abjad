from abjad.components.Container import Container
from abjad.exceptions import AssignabilityError
from abjad.components.Note import Note
from abjad.components.Rest import Rest
from abjad.tools import leaftools
from abjad.tools import listtools
from abjad.components._Tuplet import FixedDurationTuplet
import math


def make_tuplet_from_proportions_and_pair(l, (n, d), together = False):
   '''Divide `(n, d)` according to `l`.

   Where no prolation is necessary, return container. ::

      abjad> tuplettools.make_tuplet_from_proportions_and_pair([1], (7, 16))
      {c'4..}

   Where prolation is necessary, return fixed-duration tuplet. ::

      abjad> tuplettools.make_tuplet_from_proportions_and_pair([1, 2], (7, 16))
      FixedDurationTuplet(7/16, [c'8, c'4])

   ::

      abjad> tuplettools.make_tuplet_from_proportions_and_pair([1, 2, 4], (7, 16))
      FixedDurationTuplet(7/16, [c'16, c'8, c'4])

   ::

      abjad> tuplettools.make_tuplet_from_proportions_and_pair([1, 2, 4, 1], (7, 16))
      FixedDurationTuplet(7/16, [c'16, c'8, c'4, c'16])

   ::

      abjad> tuplettools.make_tuplet_from_proportions_and_pair([1, 2, 4, 1, 2], (7, 16))
      FixedDurationTuplet(7/16, [c'16, c'8, c'4, c'16, c'8])

   ::

      abjad> tuplettools.make_tuplet_from_proportions_and_pair([1, 2, 4, 1, 2, 4], (7, 16))
      FixedDurationTuplet(7/16, [c'32, c'16, c'8, c'32, c'16, c'8])

   .. note:: function accepts a pair rather than a rational.

   .. note:: function interprets `d` as tuplet denominator.

   .. versionchanged:: 1.1.2
      renamed ``divide.pair( )`` to
      ``tuplettools.make_tuplet_from_proportions_and_pair( )``.
   '''


   duration = (n, d)

   if len(l) == 0:
      raise ValueError('must divide list l of length > 0.')

   if len(l) == 1:
      if l[0] > 0:
         try:
            return Container([Note(0, duration)])
         except AssignabilityError:
            return Container(leaftools.make_notes(0, duration))
      elif l[0] < 0:
         try:
            return Container([Rest(duration)])
         except AssignabilityError:
            return Container(leaftools.make_rests(duration))
      else:
         raise ValueError('no divide zero values.')

   if len(l) > 1:
      exponent = int(math.log(listtools.weight(l), 2) - math.log(n, 2))
      denominator = int(d * 2 ** exponent)
      music = [ ]
      for x in l:
         if not x:
            raise ValueError('no divide zero values.')
         if x > 0:
            try:
               music.append(Note(0, (x, denominator)))
            except AssignabilityError:
               music.extend(leaftools.make_notes(0, (x, denominator)))
         else:
            music.append(Rest((-x, denominator)))
      return FixedDurationTuplet(duration, music)
