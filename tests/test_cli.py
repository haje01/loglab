"""cli 테스트."""
import os
from shutil import copyfile
import json

import pytest
from click.testing import CliRunner

from loglab.cli import cli, version, show, schema, verify, fetch
from loglab.version import VERSION
from loglab.util import AttrDict, request_imp_dir, test_reset


CWD = os.path.dirname(__file__)
FILE_DIR = os.path.join(CWD, 'files')


@pytest.fixture
def clear():
    test_reset()


def copy_files(files):
    # 대상 랩 파일 복사
    for fn in files:
        path = os.path.join(FILE_DIR, fn)
        assert os.path.isfile(path)
        copyfile(path, fn)


def sel_lab(labfile):
    """랩 파일 선택."""
    test_reset()
    copy_files([labfile + ".lab.json"])


def write_log(fname, body):
    """임시 로그 생성."""
    with open(fname, 'wt', encoding='utf8') as f:
        f.write(body)


def write_lab(fname, body):
    """임시 랩 파일 생성."""
    test_reset()
    if not fname.endswith('.lab.json'):
        path = fname + '.lab.json'
    with open(path, 'wt', encoding='utf8') as f:
        f.write(body)


def test_cli():
    """기본 실행 테스트."""
    runner = CliRunner()
    res = runner.invoke(cli)
    assert res.exit_code == 0
    out = res.output
    assert 'Commands:' in out
    assert 'show' in out
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
    """랩 파일 찾기 테스트."""
    runner = CliRunner()

    # 랩 파일 없이
    res = runner.invoke(show)
    assert "랩 파일이 없습니다" in res.output
    assert res.exit_code == 1

    # 랩 파일 둘 이상
    copy_files(["minimal.lab.json", "foo.lab.json"])
    res = runner.invoke(show)
    assert '하나 이상' in res.output
    assert res.exit_code == 1


def test_show():
    runner = CliRunner()

    sel_lab("minimal")
    res = runner.invoke(show)
    assert res.exit_code == 0
    out = res.output
    ans = '''Domain : foo
Description : 위대한 모바일 게임

Event : Login
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
+----------+----------+---------------+
'''
    assert ans in out

    sel_lab("foo")
    res = runner.invoke(show, ['-k'])
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
    assert ans not in out

    ans = '''Event : Login
Description : 계정 로그인
+----------+----------+-------------------+------------------------+
| Field    | Type     | Description       | Restrict               |
|----------+----------+-------------------+------------------------|
| DateTime | datetime | 이벤트 일시       |                        |
| ServerNo | integer  | 서버 번호         | 1 이상 100 미만        |
| AcntId   | integer  | 계정 ID           | 0 이상                 |
| Platform | string   | 디바이스의 플랫폼 | ['ios', 'aos'] 중 하나 |
+----------+----------+-------------------+------------------------+'''
    assert ans in out

    ans = '''Event : Logout
Description : 계정 로그아웃
+----------+----------+------------------+------------+-----------------+
| Field    | Type     | Description      | Optional   | Restrict        |
|----------+----------+------------------+------------+-----------------|
| DateTime | datetime | 이벤트 일시      |            |                 |
| ServerNo | integer  | 서버 번호        |            | 1 이상 100 미만 |
| AcntId   | integer  | 계정 ID          |            | 0 이상          |
| PlayTime | number   | 플레이 시간 (초) | True       |                 |
+----------+----------+------------------+------------+-----------------+'''
    assert ans in out

    ans = '''Event : CharLogout
Description : 캐릭터 로그아웃
+----------+----------+------------------+------------+-----------------+
| Field    | Type     | Description      | Optional   | Restrict        |
|----------+----------+------------------+------------+-----------------|
| DateTime | datetime | 이벤트 일시      |            |                 |
| ServerNo | integer  | 서버 번호        |            | 1 이상 100 미만 |
| AcntId   | integer  | 계정 ID          |            | 0 이상          |
| CharId   | integer  | 캐릭터 ID        |            | 0 이상          |
| PlayTime | number   | 플레이 시간 (초) | True       |                 |
+----------+----------+------------------+------------+-----------------+'''
    assert ans in out

    ans = '''Event : MonsterDropItem (옵션)
Description : 몬스터가 아이템을 떨어뜨림
+------------+----------+--------------------+--------------------+
| Field      | Type     | Description        | Restrict           |
|------------+----------+--------------------+--------------------|
| DateTime   | datetime | 이벤트 일시        |                    |
| ServerNo   | integer  | 서버 번호          | 1 이상 100 미만    |
| MonTypeId  | integer  | 몬스터 타입 ID     | 0 이상             |
| MonInstId  | integer  | 몬스터 인스턴스 ID | 0 이상             |
| MapId      | integer  | 맵 번호            | 0 이상             |
| PosX       | number   | 맵상 X 위치        |                    |
| PosY       | number   | 맵상 Y 위치        |                    |
| PosZ       | number   | 맵상 Z 위치        |                    |
| ItemTypeId | integer  | 아이템 타입 ID     | 1: 칼              |
|            |          |                    | 2: 방패            |
|            |          |                    | 3: 물약            |
| ItemInstId | integer  | 아이템 인스턴스 ID | 0 이상             |
| ItemName   | string   | 아이템 이름        | 7 자 이하          |
|            |          |                    | 정규식 ^Itm.* 매칭 |
+------------+----------+--------------------+--------------------+'''
    assert ans in out

    ans = '''Event : GetItem
Description : 캐릭터의 아이템 습득
+------------+----------+--------------------+--------------------+
| Field      | Type     | Description        | Restrict           |
|------------+----------+--------------------+--------------------|
| DateTime   | datetime | 이벤트 일시        |                    |
| ServerNo   | integer  | 서버 번호          | 1 이상 100 미만    |
| AcntId     | integer  | 계정 ID            | 0 이상             |
| CharId     | integer  | 캐릭터 ID          | 0 이상             |
| MapId      | integer  | 맵 번호            | 0 이상             |
| PosX       | number   | 맵상 X 위치        |                    |
| PosY       | number   | 맵상 Y 위치        |                    |
| PosZ       | number   | 맵상 Z 위치        |                    |
| ItemTypeId | integer  | 아이템 타입 ID     | 1: 칼              |
|            |          |                    | 2: 방패            |
|            |          |                    | 3: 물약            |
| ItemInstId | integer  | 아이템 인스턴스 ID | 0 이상             |
| ItemName   | string   | 아이템 이름        | 7 자 이하          |
|            |          |                    | 정규식 ^Itm.* 매칭 |
+------------+----------+--------------------+--------------------+'''
    assert ans in out

    res = runner.invoke(show, ['-c', '-k'])
    assert res.exit_code == 0
    out = res.output
    ans = '''Type : types.Id
Description : Id 타입
+------------+---------------+------------+
| BaseType   | Description   | Restrict   |
|------------+---------------+------------|
| integer    | Id 타입       | 0 이상     |
+------------+---------------+------------+

Event : Login
Description : 계정 로그인
+----------+----------+-------------------+------------------------+
| Field    | Type     | Description       | Restrict               |
|----------+----------+-------------------+------------------------|
| DateTime | datetime | 이벤트 일시       |                        |
| ServerNo | integer  | 서버 번호         | 1 이상 100 미만        |
| AcntId   | types.Id | 계정 ID           |                        |
| Platform | string   | 디바이스의 플랫폼 | ['ios', 'aos'] 중 하나 |
+----------+----------+-------------------+------------------------+
'''
    assert ans in out


def test_imp_show(clear):
    """외부 랩 파일 가져온 경우 show."""
    runner = CliRunner()

    sel_lab("boo")
    res = runner.invoke(show)
    assert res.exit_code == 1
    assert "먼저 fetch 하세요" in res.output

    url = 'https://raw.githubusercontent.com/haje01/loglab/master/tests/files/acme.lab.json'
    res = runner.invoke(fetch, [url])
    assert res.exit_code == 0

    res = runner.invoke(show, ['-k'])
    ans = '''
Domain : boo
Description : 최고의 PC 온라인 게임

Event : Login
Description : 계정 로그인
+----------+----------+---------------+---------------------------------+
| Field    | Type     | Description   | Restrict                        |
|----------+----------+---------------+---------------------------------|
| DateTime | datetime | 이벤트 일시   |                                 |
| ServerNo | integer  | 서버 번호     | 1 이상 100 미만                 |
| AcntId   | integer  | 계정 ID       | 0 이상                          |
| Platform | string   | PC의 플랫폼   | ['win', 'mac', 'linux'] 중 하나 |
+----------+----------+---------------+---------------------------------+

Event : acme.Logout
Description : 계정 로그아웃
+----------+----------+------------------+------------+-----------------+
| Field    | Type     | Description      | Optional   | Restrict        |
|----------+----------+------------------+------------+-----------------|
| DateTime | datetime | 이벤트 일시      |            |                 |
| ServerNo | integer  | 서버 번호        |            | 1 이상 100 미만 |
| AcntId   | integer  | 계정 ID          |            | 0 이상          |
| PlayTime | number   | 플레이 시간 (초) | True       |                 |
+----------+----------+------------------+------------+-----------------+
'''
    assert ans in res.output

    res = runner.invoke(show, ['-c', '-k'])
    assert res.exit_code == 0
    out = res.output
    ans = '''
Domain : boo
Description : 최고의 PC 온라인 게임

Type : acme.types.Id
Description : Id 타입
+------------+---------------+------------+
| BaseType   | Description   | Restrict   |
|------------+---------------+------------|
| integer    | Id 타입       | 0 이상     |
+------------+---------------+------------+

Event : Login
Description : 계정 로그인
+----------+---------------+---------------+---------------------------------+
| Field    | Type          | Description   | Restrict                        |
|----------+---------------+---------------+---------------------------------|
| DateTime | datetime      | 이벤트 일시   |                                 |
| ServerNo | integer       | 서버 번호     | 1 이상 100 미만                 |
| AcntId   | acme.types.Id | 계정 ID       |                                 |
| Platform | string        | PC의 플랫폼   | ['win', 'mac', 'linux'] 중 하나 |
+----------+---------------+---------------+---------------------------------+

Event : acme.Logout
Description : 계정 로그아웃
+----------+---------------+------------------+------------+-----------------+
| Field    | Type          | Description      | Optional   | Restrict        |
|----------+---------------+------------------+------------+-----------------|
| DateTime | datetime      | 이벤트 일시      |            |                 |
| ServerNo | integer       | 서버 번호        |            | 1 이상 100 미만 |
| AcntId   | acme.types.Id | 계정 ID          |            |                 |
| PlayTime | number        | 플레이 시간 (초) | True       |                 |
+----------+---------------+------------------+------------+-----------------+
'''
    assert ans in out

    res = runner.invoke(show, ['-c'])
    assert res.exit_code == 0
    out = res.output
    ans = '''
Type : acme.types.Id
Description : Id 타입
+------------+---------------+------------+
| BaseType   | Description   | Restrict   |
|------------+---------------+------------|
| integer    | Id 타입       | 0 이상     |
+------------+---------------+------------+
'''
    assert ans in out


def test_schema(clear):
    sel_lab("foo")
    runner = CliRunner()
    res = runner.invoke(schema)
    assert res.exit_code == 0
    out = res.output

    assert "foo.log.schema.json 에 로그 스키마 저장" in out
    assert "foo.flow.schema.json 에 플로우 스키마 저장" in out

    # 로그 스키마 체크
    with open(".loglab/temp/foo.log.schema.json", 'rt', encoding='utf8') as f:
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
        "pattern": "^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)(\\.[0-9]+)?(([Zz])|([\\+|\\-]([01][0-9]|2[0-3]):[0-5][0-9]))$"
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
    ans = {
        "type": "string",
        "description": "디바이스의 플랫폼",
        "enum": ["ios", "aos"]
    }
    assert defs.Login.properties.Platform == ans

    # 설명이 있는 integer enum
    ans =  {
        'type': 'integer',
        'description': '아이템 타입 ID',
        'enum': [1, 2, 3]
    }
    assert defs.GetItem.properties.ItemTypeId == ans

    # required
    ans = ["DateTime", "ServerNo", "AcntId", "Platform"]
    assert defs.Login.required == ans
    ans = ["DateTime", "ServerNo", "AcntId"]
    assert defs.Logout.required == ans


def test_verify(clear):
    sel_lab("foo")
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


def test_imp_schema(clear):
    """외부 랩 파일 가져온 경우 schema."""
    sel_lab("boo")
    runner = CliRunner()
    res = runner.invoke(schema)
    assert "먼저 fetch 하세요" in res.output

    url = 'https://raw.githubusercontent.com/haje01/loglab/master/tests/files/acme.lab.json'
    res = runner.invoke(fetch, [url])
    assert res.exit_code == 0
    out = res.output

    res = runner.invoke(schema)
    assert res.exit_code == 0
    out = res.output
    assert "boo.log.schema.json 에 로그 스키마 저장" in out
    assert "boo.flow.schema.json 에 플로우 스키마 저장" in out

    # 로그 스키마 체크
    with open(".loglab/temp/boo.log.schema.json", 'rt', encoding='utf8') as f:
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
        "pattern": "^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)(\\.[0-9]+)?(([Zz])|([\\+|\\-]([01][0-9]|2[0-3]):[0-5][0-9]))$"
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
    ans = {
        "type": "string",
        "description": "PC의 플랫폼",
        "enum": ["win", "mac", "linux"]
    }
    assert defs.Login.properties.Platform == ans

    # required
    ans = ["DateTime", "ServerNo", "AcntId", "Platform"]
    assert defs.Login.required == ans


def test_imp_verify(clear):
    """외부 랩 파일 가져온 경우 verify."""
    sel_lab("boo")
    fake_log = 'fakelog.txt'

    runner = CliRunner()
    res = runner.invoke(verify, [fake_log])
    assert res.exit_code == 1
    assert '스키마를 찾을 수 없습니다' in res.output
    res = runner.invoke(schema)


def test_fetch(clear):
    runner = CliRunner()
    url = 'https://raw.githubusercontent.com/haje01/loglab/master/tests/files/foo.lab.json'
    res = runner.invoke(fetch, [url])
    assert res.exit_code == 0
    edir = request_imp_dir()
    path = os.path.join(edir, 'foo.lab.json')
    assert os.path.isfile(path)
