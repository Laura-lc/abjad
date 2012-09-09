def timespan_2_overlaps_start_of_timespan_1(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression overlaps start of timespan::

        >>> from experimental import *

    ::

        >>> timespaninequalitytools.timespan_2_overlaps_start_of_timespan_1()
        TimespanInequality('timespan_2.start < timespan_1.start < timespan_2.stop')

    Return boolean or timespan inequality.
    '''
    from experimental import timespaninequalitytools

    timespan_inequality = timespaninequalitytools.TimespanInequality(
        'timespan_2.start < timespan_1.start < timespan_2.stop',
        timespan_1=timespan_1, 
        timespan_2=timespan_2)
    
    if timespan_inequality.is_fully_loaded and not hold: 
        return timespan_inequality()
    else:
        return timespan_inequality
