class CyclicTuple(tuple):
   '''.. versionadded:: 1.1.2

   Abjad model of cyclic tuple::

      abjad> cyclic_tuple = seqtools.CyclicList('abcd')

   ::

      abjad> cyclic_tuple
      ('a', 'b', 'c', 'd')

   ::

      abjad> for x in range(8):
      ...     print x, cyclic_tuple[x]
      ... 
      0 a
      1 b
      2 c
      3 d
      4 a
      5 b
      6 c
      7 d

   Cyclic tuples overload the item-getting method of built-in tuples.

   Cyclic tuples return a value for any integer index.

   Cyclic tuples otherwise behave exactly like built-in tuples.
   '''

   ## OVERLOADS ##

   def __getitem__(self, expr):
      if isinstance(expr, int):
         return tuple.__getitem__(self, expr % len(self))
      else:
         raise NotImplementedError('TODO: implement slice-handling.')
