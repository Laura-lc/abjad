from abjad.components._Leaf import _Leaf
from abjad.tools.iterate.naive_backward_in_expr import naive_backward_in_expr


def leaves_backward_in_expr(expr, start = 0, stop = None):
   r'''.. versionadded:: 1.1.2

   Yield right-to-left leaves in `expr`. ::

      abjad> staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
      abjad> pitchtools.diatonicize(staff)
      abjad> f(staff)
      \new Staff {
              {
                      \time 2/8
                      c'8
                      d'8
              }
              {
                      \time 2/8
                      e'8
                      f'8
              }
              {
                      \time 2/8
                      g'8
                      a'8
              }
      }

   ::

      abjad> for leaf in iterate.leaves_backward_in_expr(staff):
      ...     leaf
      ... 
      Note(a', 8)
      Note(g', 8)
      Note(f', 8)
      Note(e', 8)
      Note(d', 8)
      Note(c', 8)

   Use the optional `start` and `stop` keyword parameters to control
   the indices of iteration. ::

      abjad> for leaf in iterate.leaves_backward_in_expr(staff, start = 3):
      ...     leaf
      ... 
      Note(e', 8)
      Note(d', 8)
      Note(c', 8)

   ::

      abjad> for leaf in iterate.leaves_backward_in_expr(staff, start = 0, stop = 3):
      ...     leaf
      ... 
      Note(a', 8)
      Note(g', 8)
      Note(f', 8)

   ::

      abjad> for leaf in iterate.leaves_backward_in_expr(staff, start = 2, stop = 4):
      ...     leaf
      ... 
      Note(f', 8)
      Note(e', 8)

   .. note:: naive iteration ignores threads.

   .. versionchanged:: 1.1.2
      renamed ``iterate.leaves_backward_in( )`` to
      ``iterate.leaves_backward_in_expr( )``.
   '''

   return naive_backward_in_expr(expr, _Leaf, start = start, stop = stop)
