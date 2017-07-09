# -*- coding: utf-8 -*-
from abjad.tools import patterntools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SustainMask(AbjadValueObject):
    r'''Sustain mask.

    ..  container:: example

        ::

            >>> mask = rhythmmakertools.SustainMask(
            ...     pattern=abjad.index_every([0, 1, 7], period=16),
            ...     )

        ::

            >>> f(mask)
            rhythmmakertools.SustainMask(
                pattern=abjad.Pattern(
                    indices=[0, 1, 7],
                    period=16,
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Masks'

    __slots__ = (
        '_pattern',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        pattern=None,
        ):
        import abjad
        prototype = (
            patterntools.Pattern,
            patterntools.CompoundPattern,
            )
        if pattern is None:
            pattern = abjad.index_all()
        assert isinstance(pattern, prototype), repr(pattern)
        self._pattern = pattern

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        Returns pattern.
        '''
        return self._pattern

    ### PUBLIC METHODS ###

    @staticmethod
    def sustain(indices=None, inverted=None):
        r'''Makes sustain mask that matches `indices`.

        ..  container:: example

            Sustains divisions 1 and 2:

            ::

                >>> mask = abjad.sustain([1, 2])

            ::

                >>> f(mask)
                rhythmmakertools.SustainMask(
                    pattern=abjad.Pattern(
                        indices=[1, 2],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_all(),
                ...         mask,
                ...         ],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        ..  container:: example

            Sustains divisions -1 and -2:

            ::

                >>> mask = abjad.sustain([-1, -2])

            ::

                >>> f(mask)
                rhythmmakertools.SustainMask(
                    pattern=abjad.Pattern(
                        indices=[-1, -2],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_all(),
                ...         mask,
                ...         ],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            Works with pattern input:

            ::

                >>> pattern_1 = abjad.index_all()
                >>> pattern_2 = abjad.index_first()
                >>> pattern_3 = abjad.index_last()
                >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
                >>> mask = abjad.sustain(pattern)

            ::

                >>> f(mask)
                rhythmmakertools.SustainMask(
                    pattern=abjad.CompoundPattern(
                        (
                            abjad.Pattern(
                                indices=[0],
                                period=1,
                                ),
                            abjad.Pattern(
                                indices=[0],
                                ),
                            abjad.Pattern(
                                indices=[-1],
                                ),
                            ),
                        operator='xor',
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_all(),
                ...         mask,
                ...         ],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        ..  container:: example

            Works with pattern input and inverted flag:

            ::

                >>> pattern_1 = abjad.index_all()
                >>> pattern_2 = abjad.index_first()
                >>> pattern_3 = abjad.index_last()
                >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
                >>> mask = abjad.sustain(pattern, inverted=True)

            ::

                >>> f(mask)
                rhythmmakertools.SustainMask(
                    pattern=abjad.CompoundPattern(
                        (
                            abjad.Pattern(
                                indices=[0],
                                period=1,
                                ),
                            abjad.Pattern(
                                indices=[0],
                                ),
                            abjad.Pattern(
                                indices=[-1],
                                ),
                            ),
                        inverted=True,
                        operator='xor',
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_all(),
                ...         mask,
                ...         ],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        Returns sustain mask.
        '''
        import abjad
        indices = indices or []
        prototype = (patterntools.Pattern, patterntools.CompoundPattern)
        if isinstance(indices, prototype):
            pattern = indices
        else:
            pattern = patterntools.Pattern(
                indices=indices,
                inverted=inverted,
                )
        pattern = abjad.new(pattern, inverted=inverted)
        return SustainMask(pattern=pattern)

    @staticmethod
    def sustain_all(inverted=None):
        r'''Makes sustain mask that matches all indices.

        ..  container:: example

            Without mask:

                >>> rhythm_maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(3, 1)],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]

            ::

                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            c'4.
                            c'8
                        }
                    }
                    {
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'4.
                            c'8
                        }
                    }
                    {
                        \time 7/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            c'4.
                            c'8
                        }
                    }
                    {
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'4.
                            c'8
                        }
                    }
                }

        ..  container:: example

            With mask:

            ::

                >>> mask = abjad.sustain_all()

            ::

                >>> f(mask)
                rhythmmakertools.SustainMask(
                    pattern=abjad.Pattern(
                        indices=[0],
                        period=1,
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.TupletRhythmMaker(
                ...     division_masks=[mask],
                ...     tuplet_ratios=[(3, 1)],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]

            ::

                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        Returns sustain mask.
        '''
        pattern = patterntools.Pattern(
            indices=[0],
            inverted=inverted,
            period=1,
            )
        mask = SustainMask(pattern=pattern)
        return mask

    @staticmethod
    def sustain_every(indices, period, inverted=None):
        r'''Makes sustain mask that matches `indices` at `period`.

        ..  container:: example

            Sustains every second division:

            ::

                >>> mask = abjad.sustain_every(indices=[1], period=2)

            ::

                >>> f(mask)
                rhythmmakertools.SustainMask(
                    pattern=abjad.Pattern(
                        indices=[1],
                        period=2,
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[mask],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            Sustains every second and third division:

            ::

                >>> mask = abjad.sustain_every(indices=[1, 2], period=3)

            ::

                >>> f(mask)
                rhythmmakertools.SustainMask(
                    pattern=abjad.Pattern(
                        indices=[1, 2],
                        period=3,
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[mask],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        Returns sustain mask.
        '''
        indices = list(indices)
        pattern = patterntools.Pattern(
            indices=indices,
            inverted=inverted,
            period=period,
            )
        mask = SustainMask(pattern=pattern)
        return mask

    @staticmethod
    def sustain_first(n=1, inverted=None):
        r'''Makes sustain mask that matches the first `n` indices.

        ..  container:: example

            Sustains first division:

            ::

                >>> mask = abjad.sustain_first()

            ::

                >>> f(mask)
                rhythmmakertools.SustainMask(
                    pattern=abjad.Pattern(
                        indices=[0],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.EvenDivisionRhythmMaker(
                ...     denominators=[16],
                ...     division_masks=[mask],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \time 7/16
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                }

        ..  container:: example

            Sustains first two divisions:

            ::

                >>> mask = abjad.sustain_first(n=2)

            ::

                >>> f(mask)
                rhythmmakertools.SustainMask(
                    pattern=abjad.Pattern(
                        indices=[0, 1],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.EvenDivisionRhythmMaker(
                ...     denominators=[16],
                ...     division_masks=[mask],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                }

        Returns sustain mask.
        '''
        indices = list(range(n))
        pattern = patterntools.Pattern(
            indices=indices,
            inverted=inverted,
            )
        mask = SustainMask(pattern=pattern)
        return mask

    @staticmethod
    def sustain_last(n=1, inverted=None):
        r'''Makes sustain mask that matches the last `n` indices.

        ..  container:: example

            Sustains last division:

            ::

                >>> mask = abjad.sustain_last()

            ::

                >>> f(mask)
                rhythmmakertools.SustainMask(
                    pattern=abjad.Pattern(
                        indices=[-1],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_all(),
                ...         mask,
                ...         ],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            Sustains last two divisions:

            ::

                >>> mask = abjad.sustain_last(n=2)

            ::

                >>> f(mask)
                rhythmmakertools.SustainMask(
                    pattern=abjad.Pattern(
                        indices=[-2, -1],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_all(),
                ...         mask
                ...         ],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            Sustains no last divisions:

            ::

                >>> mask = abjad.sustain_last(n=0)

            ::

                >>> f(mask)
                rhythmmakertools.SustainMask(
                    pattern=abjad.Pattern(
                        indices=[],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_all(),
                ...         mask,
                ...         ],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        Returns sustain mask.
        '''
        indices = list(reversed(range(-1, -n-1, -1)))
        pattern = patterntools.Pattern(
            indices=indices,
            inverted=inverted,
            )
        mask = SustainMask(pattern=pattern)
        return mask
