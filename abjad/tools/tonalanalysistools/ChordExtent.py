# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class ChordExtent(AbjadObject):
    '''Chord extent. Triad, seventh chord, ninth chord, etc.

    Chord extends are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    _acceptable_number = (
        5,
        7,
        9,
        )

    _extent_number_to_extent_name = {
        5: 'triad',
        7: 'seventh',
        9: 'ninth',
        }

    ### INITIALIZER ###

    def __init__(self, number=5):
        if isinstance(number, int):
            if number not in self._acceptable_number:
                message = 'can not initialize extent: {}.'
                raise ValueError(message.format(number))
            number = number
        elif isinstance(number, type(self)):
            number = number.number
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a chord extent with number equal to that of
        this chord extent. Otherwise false.

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            if self.number == argument.number:
                return True
        return False

    def __hash__(self):
        r'''Hashes chord extent.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(ChordExtent, self).__hash__()

    def __ne__(self, argument):
        r'''Is true when chord extent does not equal `argument`. Otherwise false.

        Returns true or false.
        '''
        return not self == argument

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        r'''Name of chord extent.

        Returns string.
        '''
        return self._extent_number_to_extent_name[self.number]

    @property
    def number(self):
        r'''Number of chord extent.

        Returns nonnegative integer.
        '''
        return self._number
