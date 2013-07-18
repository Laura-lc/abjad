# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import leaftools
from abjad.tools import iterationtools
from abjad.tools.quantizationtools.AttackPointOptimizer \
	import AttackPointOptimizer


class NaiveAttackPointOptimizer(AttackPointOptimizer):
    '''Concrete ``AttackPointOptimizer`` subclass which optimizes
    attack points by fusing tie leaves within tie chains with
    leaf durations decreasing monotonically.

    ``TieChains`` will be partitioned into sub-``TieChains`` if
    leaves are found with ``TempoMarks`` attached.

    Return ``NaiveAttackPointOptimizer`` instance.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        for tie_chain in iterationtools.iterate_tie_chains_in_expr(
            expr, reverse=True):
            sub_chains = []
            current_sub_chain = []
            for leaf in tie_chain:
                tempo_marks = leaf.get_marks(contexttools.TempoMark)
                if tempo_marks:
                    if current_sub_chain:
                        current_sub_chain = \
                            leaftools.TieChain(current_sub_chain)
                        sub_chains.append(current_sub_chain)
                    current_sub_chain = []
                current_sub_chain.append(leaf)
            if current_sub_chain:
                current_sub_chain = leaftools.TieChain(current_sub_chain)
                sub_chains.append(current_sub_chain)
            for sub_chain in sub_chains:
                leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(
                    sub_chain)
