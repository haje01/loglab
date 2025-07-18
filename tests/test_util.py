import os

import pytest

from loglab.util import download, test_reset


@pytest.fixture
def clear():
    test_reset()

    # path = 'foo.lab.json'
    # download(
    #     'https://raw.githubusercontent.com/haje01/loglab/master/tests/files/foo.lab.json',
    #     path
    # )
    # assert os.path.isfile(path)
