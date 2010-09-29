from abjad import *


def test_leaftools_fuse_leaves_big_endian_01( ):
   '''Wokrs with list of leaves.'''
   fused = leaftools.fuse_leaves_big_endian(notetools.make_repeated_notes(8, Fraction(1, 4)))
   assert len(fused) == 1 
   assert fused[0].duration.written == Fraction(2)


def test_leaftools_fuse_leaves_big_endian_02( ):
   '''Works with Leaf component.'''
   fused = leaftools.fuse_leaves_big_endian([Note(0, (1, 4))])
   assert len(fused) == 1 
   assert fused[0].duration.written == Fraction(1, 4) 


def test_leaftools_fuse_leaves_big_endian_03( ):
   '''Works with containers.'''
   t = Voice(Note(0, (1, 4)) * 8)
   fused = leaftools.fuse_leaves_big_endian(t[:])
   assert len(fused) == 1 
   assert fused[0].duration.written == 2 
   assert t[0] is fused[0]


def test_leaftools_fuse_leaves_big_endian_04( ):
   '''Fusion results in tied notes.'''
   t = Voice([Note(0, (2, 16)), Note(9, (3, 16))])
   fused = leaftools.fuse_leaves_big_endian(t[:])
   assert len(fused) == 2 
   assert fused[0].duration.written == Fraction(1, 4) 
   assert fused[1].duration.written == Fraction(1, 16) 
   #assert fused[0].tie.spanner is fused[1].tie.spanner
   assert spannertools.get_the_only_spanner_attached_to_component(
      fused[0], spannertools.TieSpanner) is \
      spannertools.get_the_only_spanner_attached_to_component(
      fused[1], spannertools.TieSpanner)
   assert t[0] is fused[0]
   assert t[1] is fused[1]
   assert t[0].pitch.number == t[1].pitch.number


def test_leaftools_fuse_leaves_big_endian_05( ):
   '''Fuse leaves with differing LilyPond multipliers.'''

   t = Staff([skiptools.Skip((1, 1)), skiptools.Skip((1, 1))])
   t[0].duration.multiplier = Fraction(1, 16)
   t[1].duration.multiplier = Fraction(5, 16)

   r'''
   \new Staff {
           s1 * 1/16
           s1 * 5/16
   }
   '''

   assert t.duration.prolated == Fraction(3, 8)

   result = leaftools.fuse_leaves_big_endian(t[:])

   r'''
   \new Staff {
           s1 * 3/8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert len(result) == 1
   assert t.duration.prolated == Fraction(3, 8)
