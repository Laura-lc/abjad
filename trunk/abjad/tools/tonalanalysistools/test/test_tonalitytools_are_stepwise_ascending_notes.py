from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_are_stepwise_ascending_notes_01():

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    staff = Staff(notes)

    assert tonalanalysistools.are_stepwise_ascending_notes(staff.select_leaves())


def test_tonalanalysistools_are_stepwise_ascending_notes_02():

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    notes.reverse()
    staff = Staff(notes)

    assert not tonalanalysistools.are_stepwise_ascending_notes(staff.select_leaves())
