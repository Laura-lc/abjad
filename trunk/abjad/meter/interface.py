from abjad.core.backtracking import _BacktrackingInterface
from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.meter.meter import Meter
import types


class _MeterInterface(_Interface, _GrobHandler, _BacktrackingInterface):
   '''Handle LilyPond TimeSignature grob.
      Publish information about effective and forced meter.'''
   
   def __init__(self, client):
      '''Bind client, set forced to None and suppress to False.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TimeSignature')
      _BacktrackingInterface.__init__(self, 'meter.effective')
      self._forced = None
      self._suppress = False

   ## PRIVATE ATTRIBUTES ##

   @property
   def _selfCanContribute(self):
      r'''True when self is able to contribute LilyPond \time.'''
      return not self.suppress and (self.forced or self.change)

   @property
   def _selfShouldContribute(self):
      r'''True when self should contribute LilyPond \time.'''
      return self._selfCanContribute and not self._parentCanContribute

   @property
   def _parentCanContribute(self):
      r'''True when any parent, other than self, can contribute LP \time.'''
      for parent in self.client.parentage.parentage[1:]:
         try:
            if parent.meter._selfCanContribute:
               return True
         except AttributeError:
            pass
      return False

   ## PUBLIC ATTRIBUTES ##

   @property
   def opening(self):
      '''Format contributions at container opening or before leaf.'''
      result = [ ]
      if self._selfShouldContribute:
         result.append(self.effective.format)
      return result

   ## TODO: _MeterInterface.effective taking way too long.
   ## PROPOSAL: Derive _MeterInterface.effective from measure
   ## in parentage (if any) or metric grid (if any), otherwise
   ## return default 4/4 meter.
   ## ALTERNATIVE: Reimplement meter derivation with observer pattern.

   @property
   def effective(self):
      '''Return reference to meter effectively governing client.'''

      for x in self.client.parentage.parentage:
         if hasattr(x, 'meter') and x.meter.forced:
            return x.meter.forced
      else:
         return Meter(4, 4)

#      cur = self.client
#      while cur is not None:
#         if cur.meter.forced:
#            return cur.meter.forced
#         else:
#            ## should there be explicit measure-navigation in navigator?
#            cur = getattr(cur, 'prev', None)
#      for x in self.client.parentage.parentage[1:]:
#         if hasattr(x, 'meter') and x.meter.forced:
#            return x.meter.forced
#      return Meter(4, 4)

   @apply
   def forced( ):
      '''Read / write attribute to set meter explicitly.'''
      def fget(self):
         return self._forced
      def fset(self, arg):
         assert isinstance(arg, (Meter, types.NoneType))
         self._forced = arg
      return property(**locals( ))

   @apply
   def suppress( ):
      r'''Read / write attribute to suppress contribution
         of LilyPond \time indication at format-time.'''
      def fget(self):
         return self._suppress
      def fset(self, arg):
         assert isinstance(arg, (bool, types.NoneType))
         self._suppress = arg
      return property(**locals( ))
