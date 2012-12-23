from experimental.tools import symbolictimetools
from experimental.tools.requesttools.Request import Request


class CommandRequest(Request):
    r'''.. versionadded:: 1.0

    Request `attribute` command active at `symbolic_offset` in `voice_name`::

        >>> from experimental.tools import *

    Example. Request division command active at start of measure 4 in ``'Voice 1'``::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=1)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> measure = red_segment.select_background_measures('Voice 1', 4, 5)
        >>> command_request = measure.start_offset.request_division_command('Voice 1')

    ::

        >>> z(command_request)
        requesttools.CommandRequest(
            'divisions',
            'Voice 1',
            symbolictimetools.SymbolicOffset(
                anchor=symbolictimetools.BackgroundMeasureSelector(
                    anchor='red',
                    start_identifier=4,
                    stop_identifier=5,
                    voice_name='Voice 1'
                    )
                )
            )

    Command requested is canonically assumed to be a list or other iterable.

    Because of this the request affords list-manipulation attributes.
    These are `index`, `count`.

    Purpose of a command request is to function as a setting source.
    '''

    ### INITIALIZER ###

    def __init__(self, attribute, voice_name, symbolic_offset, modifications=None):
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(voice_name, str), repr(voice_name)
        assert isinstance(symbolic_offset, symbolictimetools.SymbolicOffset)
        Request.__init__(self, modifications=modifications)
        self._attribute = attribute
        self._voice_name = voice_name
        self._symbolic_offset = symbolic_offset

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Command request attribute specified by user.

            >>> command_request.attribute
            'divisions'

        Return string.
        '''
        return self._attribute

    @property
    def start_segment_identifier(self):
        '''Delegate to ``self.symbolic_offset.start_segment_identifier``.

            >>> command_request.start_segment_identifier
            'red'

        Return string or none.
        '''
        return self.symbolic_offset.start_segment_identifier

    @property
    def symbolic_offset(self):
        '''Command request symbolic offset specified by user.

            >>> z(command_request.symbolic_offset)
            symbolictimetools.SymbolicOffset(
                anchor=symbolictimetools.BackgroundMeasureSelector(
                    anchor='red',
                    start_identifier=4,
                    stop_identifier=5,
                    voice_name='Voice 1'
                    )
                )

        Return symbolic_offset.
        '''
        return self._symbolic_offset

    @property
    def voice_name(self):
        '''Command request voice name specified by user.

            >>> command_request.voice_name
            'Voice 1'

        Return string.
        '''
        return self._voice_name
