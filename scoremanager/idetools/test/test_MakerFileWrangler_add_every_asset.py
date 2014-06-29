# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MakerFileWrangler_add_every_asset_01():
    r'''Works in score.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    ide._session._is_repository_test = True
    input_ = 'red~example~score k rad* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_add


def test_MakerFileWrangler_add_every_asset_02():
    r'''Works in library.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    ide._session._is_repository_test = True
    input_ = 'K rad* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_add