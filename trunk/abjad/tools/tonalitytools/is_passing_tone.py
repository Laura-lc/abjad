from abjad.components.Note import Note
from abjad.tools import iterate
from abjad.tools.tonalitytools.are_scalar import are_scalar


def is_passing_tone(note):
   r'''.. versionadded:: 1.1.2

   True when `note` is both preceeded and followed by scalewise
   sibling notes. Otherwise false. ::

      abjad> t = Staff(macros.scale(4))
      abjad> for note in t:
      ...     print '%s\t%s' % (note, tonalitytools.is_passing_tone(note))
      ... 
      c'8     False
      d'8     True
      e'8     True
      f'8     False
   '''
   
   if not isinstance(note, Note):
      raise TypeError('must be note: %s' % note)

   try:
      prev_note = iterate.get_nth_namesake_from_component(note, -1) 
      next_note = iterate.get_nth_namesake_from_component(note, 1)
   except IndexError:
      return False

   return are_scalar(prev_note, note, next_note)
