# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_UserInputGetter_home_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation move home q')
    assert score_manager.session.io_transcript.signature == (11, (0, 9))