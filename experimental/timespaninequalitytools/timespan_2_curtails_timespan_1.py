def timespan_2_curtails_timespan_1(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timespan inequality indicating that `timespan_2` curtails `timespan_1`::

        >>> timespaninequalitytools.timespan_2_curtails_timespan_1()
        TimespanInequality('timespan_1.start < timespan_2.start <= timespan_1.stop <= timespan_2.stop')

    Return boolean or timespan inequality.
    '''
    from experimental import timespaninequalitytools

    timespan_inequality = timespaninequalitytools.TimespanInequality(
        'timespan_1.start < timespan_2.start <= timespan_1.stop <= timespan_2.stop',
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if timespan_inequality.is_fully_loaded and not hold:
        return timespan_inequality()
    else:
        return timespan_inequality
