# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_StylesheetFileWrangler_select_asset_path_01():

    score_manager = scoremanager.core.ScoreManager()
    wrangler = score_manager._stylesheet_file_wrangler
    wrangler._session._pending_user_input = 'clean'
    path = wrangler.select_asset_path()

    assert path == os.path.join(
        score_manager._configuration.abjad_stylesheets_directory_path,
        'clean-letter-14.ily',
        )
