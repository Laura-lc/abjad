import os
import scf


def test_DirectoryProxy_read_only_attributes_01():
    '''Named directory proxy already written to disk.
    '''

    directory_proxy = scf.proxies.DirectoryProxy(os.environ.get('SCFPATH'))
    assert directory_proxy.path_name is not None
    assert directory_proxy.is_versioned


def test_DirectoryProxy_read_only_attributes_02():

    directory_proxy_1 = scf.proxies.DirectoryProxy(os.environ.get('SCFPATH'))
    directory_proxy_2 = scf.proxies.DirectoryProxy(os.environ.get('SCFPATH'))
    directory_proxy_3 = scf.proxies.DirectoryProxy(os.environ.get('ABJAD'))

    assert     directory_proxy_1 == directory_proxy_2
    assert not directory_proxy_1 == directory_proxy_3
    assert not directory_proxy_2 == directory_proxy_3

    assert not directory_proxy_1 != directory_proxy_2
    assert     directory_proxy_1 != directory_proxy_3
    assert     directory_proxy_2 != directory_proxy_3
