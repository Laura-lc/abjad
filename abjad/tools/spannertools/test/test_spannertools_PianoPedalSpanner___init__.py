import abjad


def test_spannertools_PianoPedalSpanner___init___01():
    """
    Initialize empty piano pedal spanner.
    """

    pedal = abjad.PianoPedalSpanner()
    assert isinstance(pedal, abjad.PianoPedalSpanner)
