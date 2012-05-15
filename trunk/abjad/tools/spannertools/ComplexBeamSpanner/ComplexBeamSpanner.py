from abjad.tools import durationtools
from abjad.tools.spannertools.BeamSpanner.BeamSpanner import BeamSpanner


class ComplexBeamSpanner(BeamSpanner):
    r'''Abjad complex beam spanner::

        abjad> staff = Staff("c'16 e'16 r16 f'16 g'2")

    ::

        abjad> f(staff)
        \new Staff {
            c'16
            e'16
            r16
            f'16
            g'2
        }

    ::

        abjad> spannertools.ComplexBeamSpanner(staff[:4])
        ComplexBeamSpanner(c'16, e'16, r16, f'16)

    ::

        abjad> f(staff)
        \new Staff {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #2
            e'16 ]
            r16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            f'16 [ ]
            g'2
        }

    Return complex beam spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, components=None, lone=False, direction=None):
        BeamSpanner.__init__(self, components=components, direction=direction)
        self.lone = lone

    ### PRIVATE METHODS ###

    def _format_before_leaf(self, leaf):
        '''Spanner format contribution to output before leaf.'''
        from abjad.tools import componenttools
        result = []
        # TODO:
        #result.extend(BeamSpanner._before(self, leaf))
        result.extend(self._before(leaf))
        if componenttools.is_beamable_component(leaf):
            if self._is_my_only_leaf(leaf):
                left, right = self._get_left_right_for_lone_leaf(leaf)
            elif self._is_exterior_leaf(leaf):
                left, right = self._get_left_right_for_exterior_leaf(leaf)
            else:
                left, right = self._get_left_right_for_interior_leaf(leaf)
            if left is not None:
                result.append(r'\set stemLeftBeamCount = #%s' % left)
            if right is not None:
                result.append(r'\set stemRightBeamCount = #%s' % right)
        return result

    def _format_right_of_leaf(self, leaf):
        '''Spanner format contribution to output right of leaf.'''
        from abjad.tools import componenttools
        result = []
        #if leaf.beam.beamable:
        if componenttools.is_beamable_component(leaf):
            # lone
            if self._is_my_only_leaf(leaf):
                if self.lone:
                    if self.direction is not None:
                        result.append('%s [' % self.direction)
                    else:
                        result.append('[')
            # otherwise
            elif self._is_my_first_leaf(leaf) or not leaf._navigator._prev_bead or \
                not componenttools.is_beamable_component(leaf._navigator._prev_bead):
                if self.direction is not None:
                    result.append('%s [' % self.direction)
                else:
                    result.append('[')
            # lone
            if self._is_my_only_leaf(leaf):
                if self.lone:
                    result.append(']')
            # otherwise
            elif self._is_my_last_leaf(leaf) or not leaf._navigator._next_bead or \
                not componenttools.is_beamable_component(leaf._navigator._next_bead):
                result.append(']')
        return result

    def _get_left_right_for_exterior_leaf(self, leaf):
        '''Get left and right flag counts for exterior leaf in spanner.'''
        # lone
        if self._is_my_only_leaf(leaf):
            left, right = self._get_left_right_for_lone_leaf(leaf)
        # first
        elif self._is_my_first_leaf(leaf) or not leaf._navigator._prev_bead:
            left = 0
            right = durationtools.rational_to_flag_count(leaf.written_duration)
        # last
        elif self._is_my_last_leaf(leaf) or not leaf._navigator._next_bead:
            left = durationtools.rational_to_flag_count(leaf.written_duration)
            right = 0
        else:
            raise ValueError('leaf must be first or last in spanner.')
        return left, right

    def _get_left_right_for_interior_leaf(self, leaf):
        '''Interior leaves are neither first nor last in spanner.
        Interior leaves may be surrounded by beamable leaves.
        Interior leaves may be surrounded by unbeamable leaves.
        Four cases total for beamability of surrounding leaves.'''
        from abjad.tools import componenttools
        prev_written = leaf._navigator._prev_bead.written_duration
        cur_written = leaf.written_duration
        next_written = leaf._navigator._next_bead.written_duration
        prev_flag_count = durationtools.rational_to_flag_count(prev_written)
        cur_flag_count = durationtools.rational_to_flag_count(cur_written)
        next_flag_count = durationtools.rational_to_flag_count(next_written)
        # [unbeamable leaf beamable]
        if not componenttools.is_beamable_component(leaf._navigator._prev_bead) and \
            componenttools.is_beamable_component(leaf._navigator._next_bead):
            left = cur_flag_count
            right = min(cur_flag_count, next_flag_count)
        # [beamable leaf unbeamable]
        if componenttools.is_beamable_component(leaf._navigator._prev_bead) and \
            not componenttools.is_beamable_component(leaf._navigator._next_bead):
            left = min(cur_flag_count, prev_flag_count)
            right = cur_flag_count
        # [unbeamable leaf unbeamable]
        elif not componenttools.is_beamable_component(leaf._navigator._prev_bead) and \
            not componenttools.is_beamable_component(leaf._navigator._next_bead):
            left = cur_flag_count
            right = cur_flag_count
        # [beamable leaf beamable]
        else:
            left = min(cur_flag_count, prev_flag_count)
            right = min(cur_flag_count, next_flag_count)
            if left != cur_flag_count and right != cur_flag_count:
                left = cur_flag_count
        return left, right

    def _get_left_right_for_lone_leaf(self, leaf):
        '''Get left and right flag counts for only leaf in spanner.'''
        cur_flag_count = durationtools.rational_to_flag_count(leaf.written_duration)
        left, right = None, None
        if self.lone == 'left':
            left = cur_flag_count
            right = 0
        elif self.lone == 'right':
            left = 0
            right = cur_flag_count
        elif self.lone in ('both', True):
            left = cur_flag_count
            right = cur_flag_count
        elif self.lone in ('neither', False):
            left = None
            right = None
        else:
            raise ValueError("'lone' must be left, right, both.")
        return left, right

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def lone():
        def fget(self):
            r'''Beam lone leaf and force beam nibs to left::

                abjad> note = Note("c'16")

            ::

                abjad> beam = spannertools.ComplexBeamSpanner([note], lone = 'left')

            ::

                abjad> f(note)
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #0
                c'16 [ ]

            Beam lone leaf and force beam nibs to right::

                abjad> note = Note("c'16")

            ::

                abjad> beam = spannertools.ComplexBeamSpanner([note], lone = 'right')

            ::

                abjad> f(note)
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #2
                c'16 [ ]

            Beam lone leaf and force beam nibs to both left and right::

                abjad> note = Note("c'16")

            ::

                abjad> beam = spannertools.ComplexBeamSpanner([note], lone = 'both')

            ::

                abjad> f(note)
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #2
                c'16 [ ]

            Beam lone leaf and accept LilyPond default nibs at both left and right::

                abjad> note = Note("c'16")

            ::

                abjad> beam = spannertools.ComplexBeamSpanner([note], lone = True)

            ::

                abjad> f(note)
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #2
                c'16 [ ]

            Do not beam lone leaf::

                abjad> note = Note("c'16")

            ::

                abjad> beam = spannertools.ComplexBeamSpanner([note], lone = False)

            ::

                abjad> f(note)
                c'16

            Set to ``'left'``, ``'right'``, ``'both'``, true or false as shown above.

            Ignore this setting when spanner contains more than one leaf.
            '''
            return self._lone
        def fset(self, arg):
            assert isinstance(arg, bool) or arg in ('left', 'right', 'both')
            self._lone = arg
        return property(**locals())
