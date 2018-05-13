from abjad.enumerations import HorizontalAlignment, Right
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.systemtools.LilyPondFormatBundle import LilyPondFormatBundle


class LaissezVibrer(AbjadValueObject):
    r'''
    Laissez vibrer.

    ..  container:: example

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> laissez_vibrer = abjad.LaissezVibrer()
        >>> abjad.attach(laissez_vibrer, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            <c' e' g' c''>4
            \laissezVibrer

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _format_slot = 'right'

    _time_orientation: HorizontalAlignment = HorizontalAlignment.Right

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        r'''
        Gets string representation of laissez vibrer indicator.

        ..  container:: example

            Default:

            >>> str(abjad.LaissezVibrer())
            '\\laissezVibrer'

        '''
        return r'\laissezVibrer'

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        bundle.right.articulations.append(self._get_lilypond_format())
        return bundle
