# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_ScorePackageManager_edit_forces_tagline_01():
    r'''Quit, back, score & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup tagline q'
    score_manager._run(pending_user_input=string)
    assert score_manager._transcript.signature == (7,)

    string = 'red~example~score setup tagline b q'
    score_manager._run(pending_user_input=string)
    assert score_manager._transcript.signature == (9, (4, 7))

    string = 'red~example~score setup tagline s q'
    score_manager._run(pending_user_input=string)
    assert score_manager._transcript.signature == (9, (2, 7))

    string = 'red~example~score setup tagline h q'
    score_manager._run(pending_user_input=string)
    assert score_manager._transcript.signature == (9, (0, 7))


def test_ScorePackageManager_edit_forces_tagline_02():

    filesystem_path = os.path.join(
        configuration.abjad_score_packages_directory_path,
        'red_example_score',
        )

    try:
        score_manager = scoremanager.core.ScoreManager()
        string = 'red~example~score setup tagline for~foo~bar q'
        score_manager._run(pending_user_input=string)
        path = 'scoremanager.scores.red_example_score'
        manager = scoremanager.managers.ScorePackageManager(filesystem_path)
        assert manager._get_metadatum('forces_tagline') == 'for foo bar'
    finally:
        string = 'red~example~score setup tagline for~six~players q'
        score_manager._run(pending_user_input=string)
        path = 'scoremanager.scores.red_example_score'
        manager = scoremanager.managers.ScorePackageManager(filesystem_path)
        assert manager._get_metadatum('forces_tagline') == 'for six players'