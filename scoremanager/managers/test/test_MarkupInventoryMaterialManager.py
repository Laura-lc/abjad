# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_MarkupInventoryMaterialManager_01():

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testmarkupinventory'
    assert not score_manager._configuration.package_exists(string)
    inventory = markuptools.MarkupInventory(
        [
            markuptools.Markup(
                '\\italic { serenamente }',
                ),
            markuptools.Markup(
                '\\italic { presto }',
                )
            ],
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output_material.py',
        ]

    try:
        score_manager._run(pending_user_input=
            "lmm nmm markup testmarkupinventory "
            "omi "
            "add arg r'\\italic~{~serenamente~}' done "
            "add arg r'\\italic~{~presto~}' done done default q"
            )
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testmarkupinventory')
        manager = scoremanager.managers.ArticulationHandlerMaterialManager(
            path=path)
        assert manager._list_directory() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material == inventory
    finally:
        string = 'lmm testmarkupinventory rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testmarkupinventory'
        assert not score_manager._configuration.package_exists(string)
