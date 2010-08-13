from abjad.tools.pitchtools._CounterpointInterval import _CounterpointInterval
from abjad.tools.pitchtools._DiatonicInterval import _DiatonicInterval
from abjad.tools.pitchtools._CounterpointIntervalClass import _CounterpointIntervalClass
from abjad.tools.pitchtools._HarmonicIntervalClass import _HarmonicIntervalClass


class HarmonicCounterpointIntervalClass(_CounterpointIntervalClass, _HarmonicIntervalClass):
   '''.. versionadded:: 1.1.2

   Harmonic counterpoint interval class.
   '''

   def __init__(self, token):
      if isinstance(token, int):
         _number = token
      elif isinstance(token, (_DiatonicInterval, _CounterpointInterval)):
         _number = token.number
      if _number == 0:
         raise ValueError('must be nonzero.')
      if abs(_number) == 1:
         #self._number = 1
         _number = 1
      else:
         _number = abs(_number) % 7
         if _number == 0:
            _number = 7
         elif _number == 1:
            _number = 8
         #self._number = number
      object.__setattr__(self, '_number', _number)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, HarmonicCounterpointIntervalClass):
         if self.number == arg.number:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg
