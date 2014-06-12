# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_invoke_shell_01():
    r'''Outside of score package.
    '''

    input_ = 'g !pwd q'
    score_manager._run(input_=input_)

    path = os.path.join(
        score_manager._configuration.score_manager_directory,
        )
    string = '\n{}\n'.format(path)
    assert string in score_manager._transcript.contents


def test_SegmentPackageWrangler_invoke_shell_02():
    r'''Inside score package.
    '''

    input_ = 'red~example~score g !pwd q'
    score_manager._run(input_=input_)

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        )
    string = '\n{}\n'.format(path)
    assert string in score_manager._transcript.contents