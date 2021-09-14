"""cli 테스트."""
import os
from glob import glob
from shutil import copyfile
import json

import pytest
from click.testing import CliRunner

from loglab.cli import cli, version, doc, schema, verify
from loglab.version import VERSION
from loglab.util import AttrDict


CWD = os.path.dirname(__file__)
os.chdir(CWD)
SAMPLE_DIR = os.path.join(CWD, 'files')


@pytest.fixture
def clear():
    _clear()


def _clear():
    # 기존 파일 삭제
    for f in glob("*.lab.json"):
        os.remove(f)
    for f in glob("*.log.schema.json"):
        os.remove(f)
    for f in glob("*.flow.schema.json"):
        os.remove(f)
    for f in glob("*.txt"):
        os.remove(f)


def copy_files(files):
    # 대상 랩파일 복사
    for fn in files:
        path = os.path.join(SAMPLE_DIR, fn)
        assert os.path.isfile(path)
        copyfile(path, fn)


def sel_lab(labfile):
    """랩파일 선택."""
    _clear()
    copy_files([labfile + ".lab.json"])


def write_log(fname, body):
    """가짜 로그 생성."""
    with open(fname, 'wt') as f:
        f.write(body)


def test_cli():
    """기본 실행 테스트."""
    runner = CliRunner()
    res = runner.invoke(cli)
    assert res.exit_code == 0
    out = res.output
    assert 'Commands:' in out
    assert 'doc' in out
    assert 'dummy' in out
    assert 'schema' in out
    assert 'verify' in out
    assert 'version' in out


def test_version():
    """버전 테스트."""
    runner = CliRunner()
    res = runner.invoke(version)
    assert res.exit_code == 0
    assert res.output.strip() == VERSION


def test_labfile(clear):
    """랩파일 찾기 테스트."""
    runner = CliRunner()

    # 랩파일 없이
    res = runner.invoke(doc)
    assert "랩파일이 없습니다" in res.output
    assert res.exit_code == 1

    # 랩파일 둘 이상
    copy_files(["minimal.lab.json", "sample.lab.json"])
    res = runner.invoke(doc)
    assert '하나 이상' in res.output
    assert res.exit_code == 1


def test_doc():
    sel_lab("sample")
    runner = CliRunner()
    res = runner.invoke(doc)
    assert res.exit_code == 0
    out = res.output

    ans = '''Domain : foo
Description : 위대한 모바일 게임'''
    assert ans in out

    ans = '''Domain : foo
Description : 위대한 모바일 게임'''
    assert ans in out

    ans = '''Type : types.Id
Description : Id 타입
+------------+---------------+------------+
| BaseType   | Description   | Restrict   |
|------------+---------------+------------|
| integer    | Id 타입       | 0 이상     |
+------------+---------------+------------+'''
    assert ans in out

    ans = '''Event : Login
Description : 계정 로그인
+----------+----------+-------------------+------------------------+
| Field    | Type     | Description       | Restrict               |
|----------+----------+-------------------+------------------------|
| DateTime | datetime | 이벤트 일시       |                        |
| ServerNo | integer  | 서버 번호         | 1 이상 100 미만        |
| AcntId   | types.Id | 계정 ID           |                        |
| Platform | string   | 디바이스의 플랫폼 | ['ios', 'aos'] 중 하나 |
+----------+----------+-------------------+------------------------+'''

    ans = '''Event : Logout
Description : 계정 로그인
+----------+----------+------------------+------------+-----------------+
| Field    | Type     | Description      | Optional   | Restrict        |
|----------+----------+------------------+------------+-----------------|
| DateTime | datetime | 이벤트 일시      |            |                 |
| ServerNo | integer  | 서버 번호        |            | 1 이상 100 미만 |
| AcntId   | types.Id | 계정 ID          |            |                 |
| PlayTime | number   | 플레이 시간 (초) | true       |                 |
+----------+----------+------------------+------------+-----------------+'''
    assert ans in out

    ans = '''Event : MonsterDropItem
Description : 몬스터가 아이템을 떨어뜨림
+------------+----------+--------------------+--------------------+
| Field      | Type     | Description        | Restrict           |
|------------+----------+--------------------+--------------------|
| DateTime   | datetime | 이벤트 일시        |                    |
| ServerNo   | integer  | 서버 번호          | 1 이상 100 미만    |
| MonTypeId  | types.Id | 몬스터 타입 ID     |                    |
| MonInstId  | types.Id | 몬스터 인스턴스 ID |                    |
| MapId      | types.Id | 맵 번호            |                    |
| PosX       | number   | 맵상 X 위치        |                    |
| PosY       | number   | 맵상 Y 위치        |                    |
| PosZ       | number   | 맵상 Z 위치        |                    |
| ItemTypeId | types.Id | 아이템 타입 ID     |                    |
| ItemInstId | types.Id | 아이템 인스턴스 ID |                    |
| ItemName   | string   | 아이템 이름        | 7 자 이하          |
|            |          |                    | 정규식 ^Itm.* 매칭 |
+------------+----------+--------------------+--------------------+'''
    assert ans in out


def test_schema(clear):
    sel_lab("sample")
    runner = CliRunner()
    res = runner.invoke(schema)
    assert res.exit_code == 0
    out = res.output

    assert "foo.log.schema.json 에 로그 스키마 저장" in out
    assert "foo.flow.schema.json 에 플로우 스키마 저장" in out

    # 로그 스키마 체크
    with open("foo.log.schema.json", 'rt') as f:
        body = f.read()
        data = json.loads(body)
        scm = AttrDict(data)
        defs = scm['$defs']

    # 이벤트 타입 const
    ans = {"const": "Login"}
    assert defs.Login.properties.Event == ans

    # datetime 포맷
    ans = {
        "type": "string",
        "description": "이벤트 일시",
        "format": "date-time"
    }
    assert defs.Login.properties.DateTime == ans

    # integer 제약
    ans = {
        "type": "integer",
        "description": "서버 번호",
        "minimum": 1,
        "exclusiveMaximum": 100
    }
    assert defs.Login.properties.ServerNo == ans

    # string enum
    ans =  {
        "type": "string",
        "description": "디바이스의 플랫폼",
        "enum": ["ios", "aos"]
    }
    assert defs.Login.properties.Platform == ans

    # required
    ans = ["DateTime", "ServerNo", "AcntId", "Platform"]
    assert defs.Login.required == ans


def test_verify(clear):
    sel_lab("sample")
    fake_log = 'fakelog.txt'
    runner = CliRunner()
    res = runner.invoke(verify, [fake_log])
    assert res.exit_code == 1
    assert '스키마를 찾을 수 없습니다' in res.output
    res = runner.invoke(schema)

    log = '{"DateTime": "2021-08-1dd20:20:39", "Event": "Login", "ServerNo": 1, "AcntId": 1000, "Platform": "ios"}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, [fake_log])
    assert "does not match '^([0-9]+)" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "Login", "ServerNo": 1, "AcntId": 1000}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, [fake_log])
    assert "'Platform' is a required property" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "Login", "ServerNo": 1, "AcntId": 1000, "Platform": "win"}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, [fake_log])
    assert "'win' is not one of ['ios', 'aos']" in res.output

    log = '{"DateTime": "2021-08-13T20:21:01+09:00", "Event": "Logout", "ServerNo": 1, "AcntId": -1}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, [fake_log])
    assert "-1 is less than the minimum of 0" in res.output

    log = '{"DateTime": "2021-08-13T20:21:01+09:00", "Event": "KillMonster", "ServerNo": 1, "AcntId": 1000, "CharId": 3, "MonTypeId": 3, "MonInstId": 3, "PosX": 0, "PosY": 0, "PosZ": 0}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, [fake_log])
    assert "'MapId' is a required property" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "MonsterDropItem", "ServerNo": 1, "MonTypeId": 3, "MonInstId": 3, "MapId": 1, "PosX": 0, "PosY": 0, "PosZ": 0, "ItemTypeId": 3, "ItemInstId" 4}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, [fake_log])
    assert "유효한 JSON 형식이 아닙니다" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "MonsterDropItem", "ServerNo": 1, "MonTypeId": 3, "MonInstId": 3, "MapId": 1, "PosX": 0, "PosY": 0, "PosZ": 0, "ItemTypeId": 3, "ItemInstId": 4, "ItemName": "Sword"}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, [fake_log])
    assert "'Sword' does not match '^Itm.*'" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "MonsterDropItem", "ServerNo": 1, "MonTypeId": 3, "MonInstId": 3, "MapId": 1, "PosX": 0, "PosY": 0, "PosZ": 0, "ItemTypeId": 100, "ItemInstId": 4, "ItemName": "Sword"}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, [fake_log])
    assert "100 is not one of [1, 2, 3]" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "MonsterDropItem", "ServerNo": 1, "MonTypeId": 3, "MonInstId": 3, "MapId": 1, "PosX": 0, "PosY": 0, "PosZ": 0, "ItemTypeId": 3, "ItemInstId": 4, "ItemName": "ItmSword"}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, [fake_log])
    assert "'ItmSword' is too long" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "MonsterDropItem", "ServerNo": 1, "MonTypeId": 3, "MonInstId": 3, "MapId": 1, "PosX": 0, "PosY": 0, "PosZ": 0, "ItemTypeId": 3, "ItemInstId": 4, "ItemName": "ItmSwrd"}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, [fake_log])
    assert res.exit_code == 0
