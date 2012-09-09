def timespan_2_stops_when_timespan_1_stops(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression happens during timespan::

        >>> from experimental import *

    ::

        >>> timespaninequalitytools.timespan_2_stops_when_timespan_1_stops()
        TimespanInequality('timespan_2.stop == timespan_1.stop')

    Return boolean or timespan inequality.
    '''
    from experimental import timespaninequalitytools

    timespan_inequality = timespaninequalitytools.TimespanInequality(
        'timespan_2.stop == timespan_1.stop',
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if timespan_inequality.is_fully_loaded and not hold:
        return timespan_inequality()
    else:
        return timespan_inequality
