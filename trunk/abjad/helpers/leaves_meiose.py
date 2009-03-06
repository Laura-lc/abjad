from abjad.helpers.retroiterate import retroiterate
from abjad.helpers.spanners_detach import spanners_detach
from abjad.helpers.splice_after import splice_after
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational
import math


def leaves_meiose(expr, n = 2):
   '''Iterate expr and replace every leaf 
      with n leaves *in the same time*.
      Preserve parentage and spanners.

      Returns nothing.'''

   for leaf in retroiterate(expr, '_Leaf'):
      _leaf_meiose(leaf, n)
      


def _leaf_meiose(leaf, n = 2):
   '''Replace leaf with n instances of leaf.
      Decrease duration half for each generation.
      Preserve parentage and spanners.'''

   assert isinstance(leaf, _Leaf)
   assert int(math.log(n, 2)) == math.log(n, 2)
   assert n > 0

   new_leaves = leaf * (n - 1)
   spanners_detach(new_leaves, level = 'all')
   total_leaves = 1 + len(new_leaves)
   adjustment_multiplier = Rational(1, total_leaves)
   leaf.duration.written *= adjustment_multiplier
   for new_leaf in new_leaves:
      new_leaf.duration.written *= adjustment_multiplier
   return splice_after(leaf, new_leaves)
