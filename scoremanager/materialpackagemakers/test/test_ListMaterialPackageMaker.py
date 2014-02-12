# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ListMaterialPackageMaker_01():

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testlist')
    try:
        score_manager._run(pending_user_input=
            'materials maker list testlist '
            "17 foo done b default q "
            )
        mpp = scoremanager.materialpackagemakers.ListMaterialPackageMaker(
            'scoremanager.materialpackages.testlist')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'output_material.py',
            ]
        assert mpp.output_material == [17, 'foo']
    finally:
        score_manager._run(pending_user_input='m testlist del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testlist')