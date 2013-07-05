from abjad import *


def test_spannertools_is_component_with_spanner_attached_01():
    '''True when expr is a component with spanner attached.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = beamtools.BeamSpanner(staff.leaves)
    f(staff)

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert spannertools.is_component_with_spanner_attached(staff[0])
    assert not spannertools.is_component_with_spanner_attached(staff)


def test_spannertools_is_component_with_spanner_attached_02():
    '''True when expr is a component with spanner of class attached.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = beamtools.BeamSpanner(staff.leaves)
    f(staff)

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert spannertools.is_component_with_spanner_attached(
        staff[0], spanner_classes=(beamtools.BeamSpanner,))
        
    assert not spannertools.is_component_with_spanner_attached(
        staff[0], spanner_classes=(spannertools.SlurSpanner,))
