# -*- encoding: utf-8 -*-
import copy
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import new


class TaleaRhythmMaker(RhythmMaker):
    r'''Talea rhythm-maker.

    'Burnishing' means to forcibly cast the first or last
    (or both first and last) elements of a output cell to be
    either a note or rest.

    'Division-burnishing' rhythm-makers burnish every output cell they
    produce.

    'Output-burnishing' rhythm-makers burnish only the first and last
    output cells they produce and leave interior output cells unchanged.

    ..  container:: example

        Burnishes output:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     burnish_output=True,
            ...     lefts=(-1,),
            ...     middles=(0,),
            ...     rights=(-1,),
            ...     left_lengths=(1,),
            ...     right_lengths=(1,),
            ...     )
            >>> maker = rhythmmakertools.TaleaRhythmMaker(
            ...     talea=(1, 2, 3),
            ...     talea_denominator=16,
            ...     burnish_specifier=burnish_specifier,
            ...     prolation_addenda=(0, 2),
            ...     secondary_divisions=(9,),
            ...     )

        ::

            >>> divisions = [(3, 8), (4, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::
            
            >>> staff = maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 3/8
                    {
                        r16
                        c'8 [
                        c'8. ]
                    }
                }
                {
                    \time 4/8
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 3/5 {
                        c'16 [
                        c'8
                        c'8 ] ~
                    }
                    {
                        c'16 [
                        c'16
                        c'8 ]
                        r16
                    }
                }
            }

    '''

    r'''Example helpers:

    # used in a piece with four voices:
    # voice 1 starts reading talea at beginning of talea;
    # voice 2 starts reading talea at second event of talea;
    # voice 3 starts reading talea at third event of talea;
    # voice 4 starts reading talea at fourth event of talea.
    def helper(talea, seeds):
        assert len(seeds) == 2
        if not talea:
            return talea
        voice_index, measure_index = seeds
        talea = sequencetools.rotate_sequence(talea, -voice_index)
        return talea

    # used in a piece with four voices:
    # voice 1 starts reading talea at beginning of talea;
    # voice 2 starts reading talea 1/4 of way through talea;
    # voice 3 starts reading talea 2/4 of way through talea;
    # voice 4 starts reading talea 3/4 of way through talea.
    def quarter_rotation_helper(talea, seeds):
        assert len(seeds) == 2
        if not talea:
            return talea
        voice_index, measure_index = seeds
        index_of_rotation = -voice_index * (len(talea) // 4)
        index_of_rotation += -4 * measure_index
        talea = sequencetools.rotate_sequence(talea, index_of_rotation)
        return talea
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_burnish_specifier',
        '_helper_functions',
        '_prolation_addenda',
        '_secondary_divisions',
        '_talea',
        '_talea_denominator',
        )

    _class_name_abbreviation = 'TlRM'

    _human_readable_class_name = 'talea rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        talea=(-1, 4, -2, 3),
        talea_denominator=16,
        prolation_addenda=None,
        secondary_divisions=None,
        beam_specifier=None,
        burnish_specifier=None,
        duration_spelling_specifier=None,
        tie_specifier=None,
        helper_functions=None,
        ):
        from abjad.tools import rhythmmakertools
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            tie_specifier=tie_specifier,
            )
        prototype = (tuple, type(None))
        talea = self._to_tuple(talea)
        assert isinstance(talea, prototype)
        assert sequencetools.all_are_integer_equivalent_numbers(talea)
        self._talea = talea
        helper_functions = helper_functions or {}
        talea_helper = helper_functions.get('talea')
        prolation_addenda_helper = helper_functions.get('prolation_addenda')
        lefts_helper = helper_functions.get('lefts')
        middles_helper = helper_functions.get('middles')
        rights_helper = helper_functions.get('rights')
        left_lengths_helper = helper_functions.get('left_lengths')
        right_lengths_helper = helper_functions.get('right_lengths')
        secondary_divisions_helper = \
            helper_functions.get('secondary_divisions')
        prolation_addenda = self._to_tuple(prolation_addenda)
        burnish_specifier = burnish_specifier or \
            rhythmmakertools.BurnishSpecifier()
        assert isinstance(burnish_specifier, rhythmmakertools.BurnishSpecifier)
        self._burnish_specifier = burnish_specifier
        secondary_divisions = self._to_tuple(secondary_divisions)
        talea_helper = self._none_to_trivial_helper(talea_helper)
        prolation_addenda_helper = self._none_to_trivial_helper(
            prolation_addenda_helper)
        lefts_helper = self._none_to_trivial_helper(lefts_helper)
        middles_helper = self._none_to_trivial_helper(middles_helper)
        rights_helper = self._none_to_trivial_helper(rights_helper)
        left_lengths_helper = self._none_to_trivial_helper(
            left_lengths_helper)
        right_lengths_helper = self._none_to_trivial_helper(
            right_lengths_helper)
        secondary_divisions_helper = self._none_to_trivial_helper(
            secondary_divisions_helper)
        assert mathtools.is_positive_integer_equivalent_number(
            talea_denominator)
        assert prolation_addenda is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
                prolation_addenda)
        assert secondary_divisions is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
                secondary_divisions)
        assert callable(talea_helper)
        assert callable(prolation_addenda_helper)
        assert callable(lefts_helper)
        assert callable(middles_helper)
        assert callable(rights_helper)
        assert callable(left_lengths_helper)
        assert callable(right_lengths_helper)
        self._talea_denominator = talea_denominator
        self._prolation_addenda = prolation_addenda
        self._secondary_divisions = secondary_divisions
        if helper_functions == {}:
            helper_functions = None
        self._helper_functions = helper_functions

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls talea rhythm-maker on `divisions`.

        Returns either list of tuplets or else list of note-lists.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __format__(self, format_specification=''):
        r'''Formats talea rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            ::

                >>> print format(maker)
                rhythmmakertools.TaleaRhythmMaker(
                    talea=(1, 2, 3),
                    talea_denominator=16,
                    prolation_addenda=(0, 2),
                    secondary_divisions=(9,),
                    burnish_specifier=rhythmmakertools.BurnishSpecifier(
                        burnish_divisions=False,
                        burnish_output=True,
                        lefts=(-1,),
                        middles=(0,),
                        rights=(-1,),
                        left_lengths=(1,),
                        right_lengths=(1,),
                        ),
                    )

        Returns string.
        '''
        superclass = super(TaleaRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new talea rhythm-maker with `kwargs`.

        ..  container:: example

            ::

                >>> new_maker = new(maker, secondary_divisions=(10,))

            ::

                >>> print format(new_maker)
                rhythmmakertools.TaleaRhythmMaker(
                    talea=(1, 2, 3),
                    talea_denominator=16,
                    prolation_addenda=(0, 2),
                    secondary_divisions=(10,),
                    burnish_specifier=rhythmmakertools.BurnishSpecifier(
                        burnish_divisions=False,
                        burnish_output=True,
                        lefts=(-1,),
                        middles=(0,),
                        rights=(-1,),
                        left_lengths=(1,),
                        right_lengths=(1,),
                        ),
                    )

            ::

                >>> divisions = [(3, 8), (4, 8)]
                >>> music = new_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        {
                            r16
                            c'8 [
                            c'8. ]
                        }
                    }
                    {
                        \time 4/8
                        \times 2/3 {
                            c'16 [
                            c'8
                            c'8. ]
                        }
                        {
                            c'16 [
                            c'8 ]
                            r16
                        }
                    }
                }

        Returns new talea rhythm-maker.
        '''
        # TODO: remove custom implementation and use RhythmMaker instead.
        assert not args
        arguments = {
            'talea': self.talea,
            'talea_denominator': self.talea_denominator,
            'prolation_addenda': self.prolation_addenda,
            'burnish_specifier': copy.deepcopy(self.burnish_specifier),
            'secondary_divisions': self.secondary_divisions,
            'helper_functions': self.helper_functions,
            'beam_specifier': self.beam_specifier,
            'duration_spelling_specifier': self.duration_spelling_specifier,
            'tie_specifier': self.tie_specifier,
            }
        arguments.update(kwargs)
        maker = type(self)(**arguments)
        return maker

    ### PRIVATE METHODS ###

    def _add_ties(self, result):
        leaves = list(iterate(result).by_class(scoretools.Leaf))
        written_durations = [leaf.written_duration for leaf in leaves]
        weights = []
        for numerator in self.talea:
            duration = durationtools.Duration(
                numerator, self.talea_denominator)
            weight = abs(duration)
            weights.append(weight)
        parts = sequencetools.partition_sequence_by_weights_exactly(
            written_durations, 
            weights=weights, 
            cyclic=True, 
            overhang=True,
            )
        counts = [len(part) for part in parts]
        parts = sequencetools.partition_sequence_by_counts(leaves, counts)
        prototype = (spannertools.Tie,)
        for part in parts:
            part = selectiontools.SliceSelection(part)
            tie_spanner = spannertools.Tie()
            # this is voodoo to temporarily neuter the contiguity constraint
            tie_spanner._contiguity_constraint = None
            for component in part:
                # TODO: make top-level detach() work here
                for spanner in component._get_spanners(
                    prototype=prototype):
                    spanner._sever_all_components()
                #detach(prototype, component)
            # TODO: remove usage of Spanner._extend()
            tie_spanner._extend(part)

    def _burnish_division_part(self, division_part, token):
        assert len(division_part) == len(token)
        new_division_part = []
        for number, i in zip(division_part, token):
            if i == -1:
                new_division_part.append(-abs(number))
            elif i == 0:
                new_division_part.append(number)
            elif i == 1:
                new_division_part.append(abs(number))
            else:
                raise ValueError
        new_division_part = type(division_part)(new_division_part)
        return new_division_part

    def _burnish_all_division_parts(self, divisions, quintuplet):
        lefts, middles, rights, left_lengths, right_lengths = quintuplet
        lefts_index, rights_index = 0, 0
        burnished_divisions = []
        for division_index, division in enumerate(divisions):
            left_length = left_lengths[division_index]
            left = lefts[lefts_index:lefts_index + left_length]
            lefts_index += left_length
            right_length = right_lengths[division_index]
            right = rights[rights_index:rights_index + right_length]
            rights_index += right_length
            available_left_length = len(division)
            left_length = min([left_length, available_left_length])
            available_right_length = len(division) - left_length
            right_length = min([right_length, available_right_length])
            middle_length = len(division) - left_length - right_length
            left = left[:left_length]
            middle = middle_length * [middles[division_index]]
            right = right[:right_length]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                    division,
                    [left_length, middle_length, right_length],
                    cyclic=False,
                    overhang=False,
                    )
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_division = left_part + middle_part + right_part
            burnished_divisions.append(burnished_division)
        unburnished_weights = [mathtools.weight(x) for x in divisions]
        burnished_weights = [mathtools.weight(x) for x in burnished_divisions]
        assert burnished_weights == unburnished_weights
        return burnished_divisions

    def _burnish_division_parts(self, divisions, quintuplet):
        from abjad.tools import rhythmmakertools
        burnish_specifier = self.burnish_specifier
        if burnish_specifier is None:
            burnish_specifier = rhythmmakertools.BurnishSpecifier()
        if burnish_specifier.burnish_divisions:
            return self._burnish_all_division_parts(divisions, quintuplet)
        elif burnish_specifier.burnish_output:
            return self._burnish_first_and_last_division_parts(
                divisions, quintuplet)
        else:
            return divisions

    def _burnish_first_and_last_division_parts(self, divisions, quintuplet):
        lefts, middles, rights, left_lengths, right_lengths = quintuplet
        burnished_divisions = []
        left_length = left_lengths[0]
        left = lefts[:left_length]
        right_length = right_lengths[0]
        right = rights[:right_length]
        if len(divisions) == 1:
            available_left_length = len(divisions[0])
            left_length = min([left_length, available_left_length])
            available_right_length = len(divisions[0]) - left_length
            right_length = min([right_length, available_right_length])
            middle_length = len(divisions[0]) - left_length - right_length
            left = left[:left_length]
            middle = middle_length * [middles[0]]
            right = right[:right_length]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                    divisions[0],
                    [left_length, middle_length, right_length],
                    cyclic=False,
                    overhang=False,
                    )
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_division = left_part + middle_part + right_part
            burnished_divisions.append(burnished_division)
        else:
            # first division
            available_left_length = len(divisions[0])
            left_length = min([left_length, available_left_length])
            middle_length = len(divisions[0]) - left_length
            left = left[:left_length]
            middle = middle_length * [middles[0]]
            left_part, middle_part = \
                sequencetools.partition_sequence_by_counts(
                    divisions[0],
                    [left_length, middle_length],
                    cyclic=False,
                    overhang=False,
                    )
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            burnished_division = left_part + middle_part
            burnished_divisions.append(burnished_division)
            # middle divisions
            for division in divisions[1:-1]:
                middle_part = division
                middle = len(division) * [middles[0]]
                middle_part = self._burnish_division_part(middle_part, middle)
                burnished_division = middle_part
                burnished_divisions.append(burnished_division)
            # last division:
            available_right_length = len(divisions[-1])
            right_length = min([right_length, available_right_length])
            middle_length = len(divisions[-1]) - right_length
            right = right[:right_length]
            middle = middle_length * [middles[0]]
            middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                    divisions[-1],
                    [middle_length, right_length],
                    cyclic=False,
                    overhang=False,
                    )
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_division = middle_part + right_part
            burnished_divisions.append(burnished_division)
        unburnished_weights = [mathtools.weight(x) for x in divisions]
        burnished_weights = [mathtools.weight(x) for x in burnished_divisions]
        assert burnished_weights == unburnished_weights
        return burnished_divisions

    def _make_leaf_lists(self, numeric_map, talea_denominator):
        from abjad.tools import rhythmmakertools
        leaf_lists = []
        specifier = self.duration_spelling_specifier
        if specifier is None:
            specifier = rhythmmakertools.DurationSpellingSpecifier()
        for map_division in numeric_map:
            leaf_list = scoretools.make_leaves_from_talea(
                map_division,
                talea_denominator,
                decrease_durations_monotonically=\
                    specifier.decrease_durations_monotonically,
                forbidden_written_duration=\
                    specifier.forbidden_written_duration,
                )
            leaf_lists.append(leaf_list)
        return leaf_lists

    def _make_music(self, duration_pairs, seeds):
        from abjad.tools import rhythmmakertools
        octuplet = self._prepare_input(seeds)
        talea, prolation_addenda = octuplet[:2]
        secondary_divisions = octuplet[-1]
        taleas = (talea, prolation_addenda, secondary_divisions)
        result = self._scale_taleas(
            duration_pairs, self.talea_denominator, taleas)
        duration_pairs, lcd, talea, prolation_addenda, secondary_divisions = \
            result
        secondary_duration_pairs = self._make_secondary_duration_pairs(
            duration_pairs, secondary_divisions)
        septuplet = (talea, prolation_addenda) + octuplet[2:-1]
        numeric_map = self._make_numeric_map(
            secondary_duration_pairs, septuplet)
        leaf_lists = self._make_leaf_lists(numeric_map, lcd)
        if not prolation_addenda:
            result = leaf_lists
        else:
            tuplets = self._make_tuplets(secondary_duration_pairs, leaf_lists)
            result = tuplets
        beam_specifier = self.beam_specifier
        if beam_specifier is None:
            beam_specifier = rhythmmakertools.BeamSpecifier()
        if beam_specifier.beam_divisions_together:
            #beam = spannertools.MultipartBeam()
            #attach(beam, result)
            durations = []
            for x in result:
                duration = x.get_duration()
                durations.append(duration)
            beam = spannertools.DuratedComplexBeam(
                durations=durations,
                span_beam_count=1,
                )
            #raise Exception(result)
            #attach(beam, result)
            components = []
            for x in result:
                if isinstance(x, selectiontools.Selection):
                    components.extend(x)
                elif isinstance(x, scoretools.Tuplet):
                    components.append(x)
                else:
                    raise TypeError(x)
            attach(beam, components)
        elif beam_specifier.beam_each_division:
            for cell in result:
                beam = spannertools.MultipartBeam()
                attach(beam, cell)
        tie_specifier = self.tie_specifier
        if tie_specifier is None:
            tie_specifier = rhythmmakertools.TieSpecifier()
        if tie_specifier.tie_split_notes:
            self._add_ties(result)
        return result

    def _make_numeric_map(self, duration_pairs, septuplet):
        talea, prolation_addenda, lefts, middles, rights, left_lengths, right_lengths = septuplet
        prolated_duration_pairs = self._make_prolated_duration_pairs(
            duration_pairs, prolation_addenda)
        if isinstance(prolated_duration_pairs[0], tuple):
            prolated_numerators = [
                pair[0] for pair in prolated_duration_pairs]
        else:
            prolated_numerators = [
                pair.numerator for pair in prolated_duration_pairs]
        map_divisions = sequencetools.split_sequence_extended_to_weights(
            talea, prolated_numerators, overhang=False)
        quintuplet = (lefts, middles, rights, left_lengths, right_lengths)
        burnished_map_divisions = self._burnish_division_parts(
            map_divisions, quintuplet)
        numeric_map = burnished_map_divisions
        return numeric_map

    def _make_prolated_duration_pairs(self, duration_pairs, prolation_addenda):
        prolated_duration_pairs = []
        for i, duration_pair in enumerate(duration_pairs):
            if not prolation_addenda:
                prolated_duration_pairs.append(duration_pair)
            else:
                prolation_addendum = prolation_addenda[i]
                if hasattr(duration_pair, 'numerator'):
                    prolation_addendum %= duration_pair.numerator
                else:
                    prolation_addendum %= duration_pair[0]
                if isinstance(duration_pair, tuple):
                    numerator, denominator = duration_pair
                else:
                    numerator, denominator = duration_pair.pair
                prolated_duration_pair = (
                    numerator + prolation_addendum, denominator)
                prolated_duration_pairs.append(prolated_duration_pair)
        return prolated_duration_pairs

    def _prepare_input(self, seeds):
        helper_functions = self.helper_functions or {}
        talea = self.talea or ()
        talea_helper = helper_functions.get('talea')
        if talea_helper is not None:
            talea = talea_helper(talea, seeds)
        talea = datastructuretools.CyclicTuple(talea)

        prolation_addenda = self.prolation_addenda or ()
        prolation_addenda_helper = helper_functions.get(
            'prolation_addenda')
        if prolation_addenda_helper is not None:
            prolation_addenda = prolation_addenda_helper(
                prolation_addenda, seeds)
        prolation_addenda = datastructuretools.CyclicTuple(prolation_addenda)

        lefts = self.burnish_specifier.lefts or ()
        lefts_helper = helper_functions.get('lefts')
        if lefts_helper is not None:
            lefts = lefts_helper(lefts, seeds)
        lefts = datastructuretools.CyclicTuple(lefts)

        middles = self.burnish_specifier.middles or ()
        middles_helper = helper_functions.get('middles')
        if middles_helper is not None:
            middles = middles_helper(middles, seeds)
        middles = datastructuretools.CyclicTuple(middles)

        rights = self.burnish_specifier.rights or ()
        rights_helper = helper_functions.get('rights')
        if rights_helper is not None:
            rights = rights_helper(rights)
        rights = datastructuretools.CyclicTuple(rights)

        left_lengths = self.burnish_specifier.left_lengths or ()
        left_lengths_helper = helper_functions.get('left_lengths')
        if left_lengths_helper is not None:
            left_lengths = left_lengths_helper(left_lengths)
        left_lengths = datastructuretools.CyclicTuple(left_lengths)

        right_lengths = self.burnish_specifier.right_lengths or ()
        right_lengths_helper = helper_functions.get('right_lengths')
        if right_lengths_helper is not None:
            right_lengths = right_lengths_helper(right_lengths)
        right_lengths = datastructuretools.CyclicTuple(right_lengths)

        secondary_divisions = self.secondary_divisions or ()
        secondary_divisions_helper = helper_functions.get(
            'secondary_divisions')
        if secondary_divisions_helper is not None:
            secondary_divisions = secondary_divisions_helper(
                secondary_divisions)
        secondary_divisions = datastructuretools.CyclicTuple(
            secondary_divisions)

        return (
            talea,
            prolation_addenda,
            lefts,
            middles,
            rights,
            left_lengths,
            right_lengths,
            secondary_divisions,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def burnish_specifier(self):
        r'''Gets burnish specifier of talea rhythm-maker.

        Returns burnish specifier.
        '''
        return self._burnish_specifier

    @property
    def helper_functions(self):
        r'''Gets helper functions of talea rhythm-maker.

        Returns dictionary or none.
        '''
        return self._helper_functions

    @property
    def prolation_addenda(self):
        r'''Gets prolation addenda of talea rhythm-maker.

        Returns tuple or none.
        '''
        return self._prolation_addenda

    @property
    def secondary_divisions(self):
        r'''Gets secondary divisions of talea rhythm-maker.

        Returns tuple or none.
        '''
        return self._secondary_divisions

    @property
    def talea(self):
        r'''Gets talea of talea rhythm-maker.

        Returns tuple.
        '''
        return self._talea

    @property
    def talea_denominator(self):
        r'''Gets talea denominator of talea rhythm-maker.

        Returns positive integer.
        '''
        return self._talea_denominator

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses talea rhythm-maker.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     burnish_output=True,
                ...     lefts=(-1,),
                ...     middles=(0,),
                ...     rights=(-1,),
                ...     left_lengths=(1,),
                ...     right_lengths=(1,),
                ...     )
                >>> maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=(1, 2, 3),
                ...     talea_denominator=16,
                ...     burnish_specifier=burnish_specifier,
                ...     prolation_addenda=(0, 2),
                ...     secondary_divisions=(9,),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        {
                            r16
                            c'8 [
                            c'8. ]
                        }
                    }
                    {
                        \time 4/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'16 [
                            c'8
                            c'8 ] ~
                        }
                        {
                            c'16 [
                            c'16
                            c'8 ]
                            r16
                        }
                    }
                }

            ::

                >>> reversed_maker = maker.reverse()
                >>> print format(reversed_maker)
                rhythmmakertools.TaleaRhythmMaker(
                    talea=(3, 2, 1),
                    talea_denominator=16,
                    prolation_addenda=(2, 0),
                    secondary_divisions=(9,),
                    burnish_specifier=rhythmmakertools.BurnishSpecifier(
                        burnish_divisions=False,
                        burnish_output=True,
                        lefts=(-1,),
                        middles=(0,),
                        rights=(-1,),
                        left_lengths=(1,),
                        right_lengths=(1,),
                        ),
                    duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                        decrease_durations_monotonically=False,
                        ),
                    )

            ::

                >>> divisions = [(3, 8), (4, 8)]
                >>> music = reversed_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            r8.
                            c'8 [
                            c'16
                            c'8 ] ~
                        }
                    }
                    {
                        \time 4/8
                        {
                            c'16 [
                            c'8 ]
                        }
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/7 {
                            c'16 [
                            c'8.
                            c'8 ]
                            r16
                        }
                    }
                }

        Defined equal to copy of this talea rhythm-maker with `talea`,
        `prolation_addenda`, `secondary_divisions`, `burnish_specifier` and
        `duration_spelling_specifier` reversed.

        Returns new talea rhythm-maker.
        '''
        from abjad.tools import rhythmmakertools
        talea = tuple(reversed(self.talea))
        prolation_addenda = self.prolation_addenda
        if prolation_addenda is not None:
            prolation_addenda = tuple(reversed(prolation_addenda))
        burnish_specifier = self.burnish_specifier.reverse()
        secondary_divisions = self.secondary_divisions
        if secondary_divisions is not None:
            secondary_divisions = tuple(reversed(secondary_divisions))
        specifier = self.duration_spelling_specifier
        if specifier is None:
            specifier = rhythmmakertools.DurationSpellingSpecifier()
        specifier = specifier.reverse()
        maker = new(
            self,
            talea=talea,
            prolation_addenda=prolation_addenda,
            secondary_divisions=secondary_divisions,
            burnish_specifier=burnish_specifier,
            duration_spelling_specifier=specifier,
            )
        return maker
