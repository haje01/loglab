"""더미 로그 생성 테스트."""
import os
from shutil import copyfile
from datetime import datetime

import pytest
from click.testing import CliRunner

from loglab.util import test_reset
from loglab.cli import schema
from loglab.dummy import generate_dummy_sync
from loglab.schema import verify_labfile

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

    lab = verify_labfile('foo.lab.json')

    flow = {
        "labfile": "foo.lab.json",
    }
    data = generate_dummy_sync(lab, flow)
    assert data == {
        'foo.txt': []
    }

    flow = {
        "labfile": "foo.lab.json",
        "file_by": ["ServerNo", [1, 2]]
    }
    with pytest.raises(Exception, match='file_ptrn'):
        data = generate_dummy_sync(lab, flow)

    flow = {
        "labfile": "foo.lab.json",
        "file_ptrn": "foo_%Y%m%d_{ServerNo:03d}.txt"
    }
    with pytest.raises(KeyError, match='ServerNo'):
        data = generate_dummy_sync(lab, flow)

    flow = {
        "labfile": "foo.lab.json",
        "file_by": ["ServerNo", [1, 2]],
        "file_ptrn": "foo_%Y%m%d_{ServerNo:03d}.txt"
    }
    today = datetime.today()
    ptrn = today.strftime('foo_%Y%m%d_{ServerNo:03d}.txt')
    data = generate_dummy_sync(lab, flow)
    assert data == {
        ptrn.format(ServerNo=1): [],
        ptrn.format(ServerNo=2): [],
    }

    flow = {
        "labfile": "foo.lab.json",
        "file_ptrn": "foo_%Y%m%d.txt",
        "datetime": {
            "start": "2021-10-20 13"
        }
    }
    data = generate_dummy_sync(lab, flow)
    assert data == {
        'foo_20211020.txt': []
    }

    flow = {
        "labfile": "foo.lab.json",
        "file_by": ["ServerNo", [1, 2]],
        "file_ptrn": "foo_%Y%m%d_{ServerNo:03d}.txt",
        "datetime": {
            "start": "2021-10-20 13"
        }
    }
    data = generate_dummy_sync(lab, flow)
    assert data == {
        'foo_20211020_001.txt': [], 
        'foo_20211020_002.txt': []
    }

    flow = {
        "labfile": "foo.lab.json",
        "datetime": {
            "start": "2021-10-20 13",
            "tzoffset": "+09:00"
        },
        "flow": {
            "steps": [
                "Login",
                "Logout"
            ]
        }
    }
    data = generate_dummy_sync(lab, flow)
    assert data == {
        'foo.txt': [
            {"DateTime": "2021-10-20T13:00:00+09:00", "Event": "Login"},
            {"DateTime": "2021-10-20T13:00:01+09:00", "Event": "Logout"}
        ]
    }
    # assert data == {
    #     "foo_001_20211020.txt": [
    #         {
    #             "DateTime": "2021-10-20T13:00:00+09:00",
    #             "Event": "Login",
    #             "ServerNo": 1,
    #             "Account": 1
    #         },
    #         {
    #             "DateTime": "2021-10-20T13:00:00+09:00",
    #             "Event": "Login",
    #             "ServerNo": 1,
    #             "Account": 2
    #         },
    #         {
    #             "DateTime": "2021-10-20T13:00:02+09:00",
    #             "Event": "Logout",
    #             "ServerNo": 1,
    #             "Account": 1
    #         },
    #         {
    #             "DateTime": "2021-10-20T13:00:02+09:00",
    #             "Event": "Logout",
    #             "ServerNo": 1,
    #             "Account": 2
    #         }
    #     ],
    #     "foo_002_20211020.txt": [
    #         {
    #             "DateTime": "2021-10-20T13:00:00+09:00",
    #             "Event": "Login",
    #             "ServerNo": 2,
    #             "Account": 1
    #         },
    #         {
    #             "DateTime": "2021-10-20T13:00:00+09:00",
    #             "Event": "Login",
    #             "ServerNo": 2,
    #             "Account": 2
    #         },
    #         {
    #             "DateTime": "2021-10-20T13:00:02+09:00",
    #             "Event": "Logout",
    #             "ServerNo": 2,
    #             "Account": 1
    #         },
    #         {
    #             "DateTime": "2021-10-20T13:00:02+09:00",
    #             "Event": "Logout",
    #             "ServerNo": 2,
    #             "Account": 2
    #         }
    #     ]
    # }
