# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class AltoVoice(Instrument):
    r'''A alto voice.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> alto = instrumenttools.AltoVoice()
        >>> attach(alto, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Alto }
            \set Staff.shortInstrumentName = \markup { Alto }
            c'4
            d'4
            e'4
            fs'4
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = 'alto'

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='alto',
        short_instrument_name='alto',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[F3, G5]',
        sounding_pitch_of_written_middle_c=None,
        ):
        Instrument.__init__(
            self,
            instrument_name=instrument_name,
            short_instrument_name=short_instrument_name,
            instrument_name_markup=instrument_name_markup,
            short_instrument_name_markup=short_instrument_name_markup,
            allowable_clefs=allowable_clefs,
            pitch_range=pitch_range,
            sounding_pitch_of_written_middle_c=\
                sounding_pitch_of_written_middle_c,
            )
        self._performer_names.extend([
            'vocalist',
            'alto',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets alto's allowable clefs.

        ..  container:: example

            ::

                >>> alto.allowable_clefs
                ClefInventory([Clef('treble')])

            ::

                >>> show(alto.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets alto's name.

        ..  container:: example

            ::

                >>> alto.instrument_name
                'alto'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets alto's instrument name markup.

        ..  container:: example

            ::

                >>> alto.instrument_name_markup
                Markup(('Alto',))

            ::

                >>> show(alto.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets alto's range.

        ..  container:: example

            ::

                >>> alto.pitch_range
                PitchRange('[F3, G5]')

            ::

                >>> show(alto.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets alto's short instrument name.

        ..  container:: example

            ::

                >>> alto.short_instrument_name
                'alto'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets alto's short instrument name markup.

        ..  container:: example

            ::

                >>> alto.short_instrument_name_markup
                Markup(('Alto',))

            ::

                >>> show(alto.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of alto's written middle C.

        ..  container:: example

            ::

                >>> alto.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(alto.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)