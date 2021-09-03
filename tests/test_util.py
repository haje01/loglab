import os

import pytest

from loglab.util import verify_labfile, LOGLAB_HOME


def test_verify():
    # 로컬 스키마로 검증
    labfile = os.path.join(LOGLAB_HOME, "tests/test.lab.json")
    verify_labfile(labfile)

    # 원격 스키마로 검증
    scmuri = "https://raw.githubusercontent.com/haje01/loglab/master/schema/lab.schema.json"
    verify_labfile(labfile, scmuri)
