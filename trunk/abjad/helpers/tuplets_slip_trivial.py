from abjad.helpers.bequeath import bequeath
from abjad.tools import iterate


def tuplets_slip_trivial(expr):
   '''Iterate expr. Slip each trivial tuplet in expr out of score.
      Return None because processes potentially many trivial tuplets.'''
   
   from abjad.tuplet.tuplet import _Tuplet
   for tuplet in list(iterate.naive(expr, _Tuplet)):
      if tuplet.trivial:
         bequeath([tuplet], tuplet[:])
