def get_spanner_format_contributions(leaf, slot):
    '''.. versionadded:: 2.0

    Get spanner format contributions for `leaf` at `slot`.

    Return list.
    '''
    from abjad.tools import spannertools

    result = []
    spanners = spannertools.get_spanners_attached_to_any_improper_parent_of_component(leaf)
    spanners = list(spanners)
    spanners.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
    if slot == 'before':
        for spanner in spanners:
            spanner_contributions = []
            if spanner._is_my_first_leaf(leaf):
                contributions = spanner.override._list_format_contributions('override', is_once = False)
                spanner_contributions.extend(contributions)
            if hasattr(spanner, '_format_before_leaf'):
                spanner_contributions.extend(spanner._format_before_leaf(leaf))
            else:
                spanner_contributions.extend(spanner._format._before(leaf))
            result.extend(spanner_contributions)
    elif slot == 'after':
        for spanner in spanners:
            spanner_contributions = []
            if hasattr(spanner, '_format_after_leaf'):
                spanner_contributions.extend(spanner._format_after_leaf(leaf))
            else:
                spanner_contributions.extend(spanner._format._after(leaf))
            if spanner._is_my_last_leaf(leaf):
                contributions = spanner.override._list_format_contributions('revert')
                spanner_contributions.extend(contributions)
            result.extend(spanner_contributions)
    elif slot == 'right':
        stop_contributions, other_contributions = [], []
        for spanner in spanners:
            if hasattr(spanner, '_format_right_of_leaf'):
                contributions = spanner._format_right_of_leaf(leaf)
            else:
                contributions = spanner._format._right(leaf)
            if contributions:
                if spanner._is_my_last_leaf(leaf):
                    stop_contributions.extend(contributions)
                else:
                    other_contributions.extend(contributions)
        result = stop_contributions + other_contributions
    return ['spanners', result]
