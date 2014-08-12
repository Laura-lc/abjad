# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.handlertools.DynamicHandler import DynamicHandler


class NoteAndChordHairpinHandler(DynamicHandler):
    r'''Note and chord hairpin handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_hairpin_token',
        )

    ### INITIALIZER ###

    def __init__(self, hairpin_token=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        if hairpin_token is not None:
            assert spannertools.Hairpin._is_hairpin_token(hairpin_token)
        self._hairpin_token = hairpin_token

    ### SPECIAL METHODS ###

    def __call__(self, expr, offset=0):
        r'''Calls note and chord hairpin handler on `expr` with `offset`.

        Returns none.
        '''
        leaves = list(iterate(expr).by_class(scoretools.Leaf))
        leaves = self._remove_outer_rests_from_sequence(leaves)
        #group = leaves
        group = selectiontools.SliceSelection(leaves)
        is_short_group = False
        if len(group) == 1:
            is_short_group = True
        elif self.minimum_duration is not None:
            if group.duration < self.minimum_duration:
                is_short_group = True
        if is_short_group:
            start_dynamic = self.hairpin_token[0]
            #indicatortools.Dynamic(start_dynamic)(group[0])
            command = indicatortools.LilyPondCommand(start_dynamic, 'right')
            attach(command, group[0])
        else:
            descriptor = ' '.join([x for x in self.hairpin_token if x])
            hairpin = spannertools.Hairpin(
                descriptor=descriptor,
                include_rests=False,
                )
            attach(hairpin, group)
        return expr

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='hairpin_token',
                command='ht',
                editor=idetools.getters.get_hairpin_token,
                ),
            systemtools.AttributeDetail(
                name='minimum_duration',
                command='md',
                editor=idetools.getters.get_duration,
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def hairpin_token(self):
        r'''Gets hairpin token of handler.

        Returns string or none.
        '''
        return self._hairpin_token