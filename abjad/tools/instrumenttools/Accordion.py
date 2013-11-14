# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.Instrument import Instrument


class Accordion(Instrument):
    r'''An accordion.

    ::

        >>> piano_staff = scoretools.PianoStaff()
        >>> piano_staff.append(Staff("c'8 d'8 e'8 f'8"))
        >>> piano_staff.append(Staff("c'4 b4"))
        >>> accordion = instrumenttools.Accordion()
        >>> attach(accordion, piano_staff)
        >>> show(piano_staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(piano_staff)
        \new PianoStaff <<
            \set PianoStaff.instrumentName = \markup { Accordion }
            \set PianoStaff.shortInstrumentName = \markup { Acc. }
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                c'4
                b4
            }
        >>

    The accordion targets the piano staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._target_context = scoretools.PianoStaff
        self._default_allowable_clefs = marktools.ClefInventory([
            marktools.Clef('treble'),
            marktools.Clef('bass'),
            ])
        self._default_instrument_name = 'accordion'
        self._default_performer_names.extend([
            'keyboardist',
            'accordionist',
            ])
        self._default_pitch_range = pitchtools.PitchRange(-32, 48)
        self._default_short_instrument_name = 'acc.'
        self._default_starting_clefs = marktools.ClefInventory([
            marktools.Clef('treble'),
            marktools.Clef('bass'),
            ])
        self._is_primary_instrument = True

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats accordion.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            Without customization:

            ::

                >>> accordion = instrumenttools.Accordion()
                >>> print format(accordion)
                instrumenttools.Accordion()

        ..  container:: example

            With customization:

            ::

                >>> custom = instrumenttools.Accordion()
                >>> custom.instrument_name = 'fisarmonica'
                >>> markup = markuptools.Markup('Fisarmonica')
                >>> custom.instrument_name_markup = markup
                >>> custom.short_instrument_name = 'fis.'
                >>> markup = markuptools.Markup('Fis.')
                >>> custom.short_instrument_name_markup = markup
                >>> custom.allowable_clefs = ['treble']
                >>> custom.pitch_range = '[C4, C6]'
                >>> custom.sounding_pitch_of_written_middle_c = "c''"

            ::

                >>> print format(custom)
                instrumenttools.Accordion(
                    instrument_name='fisarmonica',
                    instrument_name_markup=markuptools.Markup(
                        ('Fisarmonica',)
                        ),
                    short_instrument_name='fis.',
                    short_instrument_name_markup=markuptools.Markup(
                        ('Fis.',)
                        ),
                    allowable_clefs=marktools.ClefInventory(
                        [
                            marktools.Clef(
                                'treble'
                                ),
                            ]
                        ),
                    pitch_range=pitchtools.PitchRange(
                        '[C4, C6]'
                        ),
                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch("c''"),
                    )

        Returns string.
        '''
        superclass = super(Accordion, self)
        return superclass.__format__(format_specification=format_specification)

    ### PUBLIC PROPERTIES ###

    @apply
    def allowable_clefs():
        def fget(self):
            r'''Gets and sets allowable clefs.

            ..  container:: example

                Gets property:

                ::

                    >>> accordion.allowable_clefs
                    ClefInventory([Clef('treble'), Clef('bass')])

                ::

                    >>> show(accordion.allowable_clefs) # doctest: +SKIP

            ..  container:: example

                Sets property:

                ::

                    >>> accordion.allowable_clefs = ['treble']
                    >>> accordion.allowable_clefs
                    ClefInventory([Clef('treble')])

                ::

                    >>> show(accordion.allowable_clefs) # doctest: +SKIP

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.allowable_clefs = None
                    >>> accordion.allowable_clefs
                    ClefInventory([Clef('treble'), Clef('bass')])

                ::

                    >>> show(accordion.allowable_clefs) # doctest: +SKIP

            Returns clef inventory.
            '''
            return Instrument.allowable_clefs.fget(self)
        def fset(self, allowable_clefs):
            return Instrument.allowable_clefs.fset(self, allowable_clefs)
        return property(**locals())

    @apply
    def instrument_name():
        def fget(self):
            r'''Gets and sets instrument name.

            ..  container:: example

                Gets property:

                ::

                    >>> accordion.instrument_name
                    'accordion'

            ..  container:: example

                Sets property:

                ::

                    >>> accordion.instrument_name = 'fisarmonica'
                    >>> accordion.instrument_name
                    'fisarmonica'

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.instrument_name = None
                    >>> accordion.instrument_name
                    'accordion'

            Returns string.
            '''
            return Instrument.instrument_name.fget(self)
        def fset(self, foo):
            Instrument.instrument_name.fset(self, foo)
        return property(**locals())

    @apply
    def instrument_name_markup():
        def fget(self):
            r'''Gets and sets instrument name markup.

            ..  container:: example

                Gets property:

                ::

                    >>> accordion.instrument_name_markup
                    Markup(('Accordion',))

                ::

                    >>> show(accordion.instrument_name_markup) # doctest: +SKIP

            ..  container:: example

                Sets property:

                ::

                    >>> markup = markuptools.Markup('Fisarmonica')
                    >>> accordion.instrument_name_markup = markup
                    >>> accordion.instrument_name_markup
                    Markup(('Fisarmonica',))

                ::

                    >>> show(accordion.instrument_name_markup) # doctest: +SKIP

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.instrument_name_markup = None
                    >>> accordion.instrument_name_markup
                    Markup(('Accordion',))

                ::

                    >>> show(accordion.instrument_name_markup) # doctest: +SKIP

            Returns markup.
            '''
            return Instrument.instrument_name_markup.fget(self)
        def fset(self, markup):
            return Instrument.instrument_name_markup.fset(self, markup)
        return property(**locals())

    @apply
    def pitch_range():
        def fget(self):
            r"""Gets and sets pitch range.

            ..  container:: example

                Gets property:

                ::

                    >>> accordion.pitch_range
                    PitchRange('[E1, C8]')

                ::

                    >>> show(accordion.pitch_range) # doctest: +SKIP

            ..  container:: example

                Sets property:

                ::

                    >>> accordion.pitch_range = '[C2, C6]'
                    >>> accordion.pitch_range
                    PitchRange('[C2, C6]')

                ::

                    >>> show(accordion.pitch_range) # doctest: +SKIP

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.pitch_range = None
                    >>> accordion.pitch_range
                    PitchRange('[E1, C8]')

                ::

                    >>> show(accordion.pitch_range) # doctest: +SKIP

            Returns pitch range.
            """
            return Instrument.pitch_range.fget(self)
        def fset(self, pitch_range):
            Instrument.pitch_range.fset(self, pitch_range)
        return property(**locals())

    @apply
    def short_instrument_name():
        def fget(self):
            r'''Gets and sets short instrument name.

            ..  container:: example

                Gets property:

                ::

                    >>> accordion.short_instrument_name
                    'acc.'

            ..  container:: example

                Sets property:

                ::

                    >>> accordion.short_instrument_name = 'fis.'
                    >>> accordion.short_instrument_name
                    'fis.'

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.short_instrument_name = None
                    >>> accordion.short_instrument_name
                    'acc.'

            Returns string.
            '''
            return Instrument.short_instrument_name.fget(self)
        def fset(self, name):
            return Instrument.short_instrument_name.fset(self, name)
        return property(**locals())

    @apply
    def short_instrument_name_markup():
        def fget(self):
            r'''Gets and sets short instrument name markup.

            ..  container:: example

                Gets property:

                ::

                    >>> accordion.short_instrument_name_markup
                    Markup(('Acc.',))

                ::

                    >>> show(accordion.short_instrument_name_markup) # doctest: +SKIP

            ..  container:: example

                Sets property:

                ::

                    >>> markup = markuptools.Markup('fis.')
                    >>> accordion.short_instrument_name_markup = markup
                    >>> accordion.short_instrument_name_markup
                    Markup(('fis.',))

                ::

                    >>> show(accordion.short_instrument_name_markup) # doctest: +SKIP

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.short_instrument_name_markup = None
                    >>> accordion.short_instrument_name_markup
                    Markup(('Acc.',))

                ::

                    >>> show(accordion.short_instrument_name_markup) # doctest: +SKIP

            Returns markup.
            '''
            return Instrument.short_instrument_name_markup.fget(self)
        def fset(self, markup):
            return Instrument.short_instrument_name_markup.fset(self, markup)
        return property(**locals())

    @apply
    def sounding_pitch_of_written_middle_c():
        def fget(self):
            r'''Gets and sets sounding pitch of written middle C.

            ..  container:: example

                Gets property:

                ::

                    >>> accordion.sounding_pitch_of_written_middle_c
                    NamedPitch("c'")

                ::

                    >>> show(accordion.sounding_pitch_of_written_middle_c) # doctest: +SKIP

            ..  container:: example

                Sets property:

                ::

                    >>> accordion.sounding_pitch_of_written_middle_c = 'cs'
                    >>> accordion.sounding_pitch_of_written_middle_c
                    NamedPitch('cs')

                ::

                    >>> show(accordion.sounding_pitch_of_written_middle_c) # doctest: +SKIP

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.sounding_pitch_of_written_middle_c = None
                    >>> accordion.sounding_pitch_of_written_middle_c
                    NamedPitch("c'")

                ::

                    >>> show(accordion.sounding_pitch_of_written_middle_c) # doctest: +SKIP

            Returns named pitch.
            '''
            return Instrument.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, pitch):
            Instrument.sounding_pitch_of_written_middle_c.fset(self, pitch)
        return property(**locals())
