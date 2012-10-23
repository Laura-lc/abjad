import fractions
import math
from abjad.tools import mathtools


def rational_to_equal_or_lesser_assignable_rational(rational):
    '''.. versionadded:: 1.1

    Change `rational` to equal or lesser assignable rational::

        >>> from abjad.tools import durationtools

    ::

        >>> for n in range(1, 17):
        ...     rational = Duration(n, 16)
        ...     written = durationtools.rational_to_equal_or_lesser_assignable_rational(rational)
        ...     print '%s/16\t%s' % (n, written)
        ...
        1/16    1/16
        2/16    1/8
        3/16    3/16
        4/16    1/4
        5/16    1/4
        6/16    3/8
        7/16    7/16
        8/16    1/2
        9/16    1/2
        10/16   1/2
        11/16   1/2
        12/16   3/4
        13/16   3/4
        14/16   7/8
        15/16   15/16
        16/16   1

    Return fraction.

    Function returns dotted and double dotted durations where possible.

    .. versionchanged:: 2.0
        Fixed to produce monotonically increasing output
        in response to monotonically increasing input.

    .. versionchanged:: 2.0
        renamed ``durationtools.prolated_to_written_not_greater_than()`` to
        ``durationtools.rational_to_equal_or_lesser_assignable_rational()``.
    '''
    from abjad.tools import durationtools

    # check input
    rational = durationtools.Duration(rational)

    good_denominator = mathtools.least_power_of_two_greater_equal(rational.denominator)

    cur_numerator = rational.numerator
    candidate = durationtools.Duration(cur_numerator, good_denominator)

    while not candidate.is_assignable:
        cur_numerator -= 1
        candidate = durationtools.Duration(cur_numerator, good_denominator)

    return candidate
