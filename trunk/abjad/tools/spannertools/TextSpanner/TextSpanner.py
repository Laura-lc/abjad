from abjad.tools.spannertools.Spanner import Spanner


class TextSpanner(Spanner):
    r'''.. versionadded:: 2.0

    Abjad text spanner::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> text_spanner = spannertools.TextSpanner(staff[:])

    ::

        abjad> markup = markuptools.Markup('(markup #:bold #:italic "foo")', style_string = 'scheme')
        abjad> text_spanner.override.text_spanner.bound_details__left__text = markup
        abjad> markup = markuptools.Markup("(markup #:draw-line '(0 . -1))", style_string = 'scheme')
        abjad> text_spanner.override.text_spanner.bound_details__right__text = markup
        abjad> text_spanner.override.text_spanner.dash_fraction = 1

    ::

        abjad> f(staff)
        \new Staff {
            \override TextSpanner #'bound-details #'left #'text = #(markup #:bold #:italic "foo")
            \override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . -1))
            \override TextSpanner #'dash-fraction = #1
            c'8 \startTextSpan
            d'8
            e'8
            f'8 \stopTextSpan
            \revert TextSpanner #'bound-details #'left #'text
            \revert TextSpanner #'bound-details #'right #'text
            \revert TextSpanner #'dash-fraction
        }

    Override LilyPond TextSpanner grob.

    Return text spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, components = None):
        Spanner.__init__(self, components)

    ### PRIVATE METHODS ###

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r'\startTextSpan')
        if self._is_my_last_leaf(leaf):
            result.append(r'\stopTextSpan')
        return result
