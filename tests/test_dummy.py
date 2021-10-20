"""더미 로그 생성 테스트."""
import os
from shutil import copyfile

import pytest
from click.testing import CliRunner

from loglab.util import test_reset
from loglab.cli import schema
from loglab.dummy import generate_dummy_sync

CWD = os.path.dirname(__file__)
FILE_DIR = os.path.join(CWD, 'files')


@pytest.fixture
def clear():
    test_reset()


def copy_files(files):
    # 테스트용  파일 복사
    for fn in files:
        path = os.path.join(FILE_DIR, fn)
        assert os.path.isfile(path)
        copyfile(path, fn)


def test_dummy(clear):
    runner = CliRunner()
    copy_files(['foo.lab.json'])

    res = runner.invoke(schema, 'foo.lab.json')
    assert res.exit_code == 0
    out = res.output

    assert "foo.log.schema.json 에 로그 스키마 저장" in out
    assert "foo.flow.schema.json 에 플로우 스키마 저장" in out

    flow = {
        "labfile": "/home/ubuntu/loglab_test/foo.lab.json",
        "file_id": "ServerNo",
        "file_cnt": 2,
        "file_ptrn": "foo_{id}_%Y%m%d.jsonl",
        "flow": {
            "spawn_id": "AcntId",
            "spawn_cnt": 2,
            "steps": [
                "Login",
                "Logout"
            ]
        }
    }

    generate_dummy_sync(flow)
