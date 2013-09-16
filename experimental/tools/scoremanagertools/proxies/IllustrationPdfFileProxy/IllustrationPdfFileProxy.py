# -*- encoding: utf-8 -*-
import os
from abjad.tools import iotools
from experimental.tools.scoremanagertools.proxies.FileProxy import FileProxy


class IllustrationPdfFileProxy(FileProxy):

    ### CLASS VARIABLES ###

    extension = '.pdf'

    ### PUBLIC METHODS ###

    def interactively_view(self):
        command = 'open {}'.format(self.filesystem_path)
        iotools.spawn_subprocess(command)
