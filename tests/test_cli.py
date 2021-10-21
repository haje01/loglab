"""cli 테스트."""
import os
from shutil import copyfile
import json
from shutil import rmtree

import pytest
from click.testing import CliRunner

from loglab.cli import cli, version, show, schema, verify
from loglab.version import VERSION
from loglab.util import AttrDict, test_reset


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


def write_log(fname, body):
    """임시 로그 생성."""
    with open(fname, 'wt', encoding='utf8') as f:
        f.write(body)


# def write_lab(fname, body):
#     """임시 랩 파일 생성."""
#     test_reset()
#     if not fname.endswith('.lab.json'):
#         path = fname + '.lab.json'
#     with open(path, 'wt', encoding='utf8') as f:
#         f.write(body)


def test_cli():
    """기본 실행 테스트."""
    runner = CliRunner()
    res = runner.invoke(cli)
    assert res.exit_code == 0
    out = res.output
    assert 'Commands:' in out
    assert 'show' in out
    assert 'schema' in out
    assert 'verify' in out
    assert 'version' in out


def test_version():
    """버전 테스트."""
    runner = CliRunner()
    res = runner.invoke(version)
    assert res.exit_code == 0
    assert res.output.strip() == VERSION


# def test_labfile():
#     """랩 파일 찾기 테스트."""
#     runner = CliRunner()

#     # 랩 파일 없이
#     res = runner.invoke(show)
#     assert "랩 파일이 없습니다" in res.output
#     assert res.exit_code == 1

#     # 랩 파일 둘 이상
#     copy_files(["minimal.lab.json", "foo.lab.json"])
#     res = runner.invoke(show)
#     assert '하나 이상' in res.output
#     assert res.exit_code == 1


def test_show(clear):
    runner = CliRunner()

    copy_files(['minimal.lab.json', 'foo.lab.json'])
    res = runner.invoke(show, ['minimal.lab.json'])
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

    res = runner.invoke(show, ['foo.lab.json', '-k'])
    assert res.exit_code == 0
    out = res.output

    ans = '''Domain : foo
Description : 위대한 모바일 게임'''
    assert ans in out

    ans = '''Domain : foo
Description : 위대한 모바일 게임'''
    assert ans in out

    ans = '''Type : types.unsigned
Description : Id 타입
+------------+---------------+------------+
| BaseType   | Description   | Restrict   |
|------------+---------------+------------|
| integer    | Id 타입       | 0 이상     |
+------------+---------------+------------+'''
    assert ans not in out

    ans = '''Event : Login
Description : 계정 로그인
+----------+----------+-------------------+------------------+
| Field    | Type     | Description       | Restrict         |
|----------+----------+-------------------+------------------|
| DateTime | datetime | 이벤트 일시       |                  |
| ServerNo | integer  | 서버 번호         | 1 이상 100 미만  |
| AcntId   | integer  | 계정 ID           | 0 이상           |
| Platform | string   | 디바이스의 플랫폼 | ios, aos 중 하나 |
+----------+----------+-------------------+------------------+'''
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
+-----------+----------+------------------+------------------------------------+
| Field     | Type     | Description      | Restrict                           |
|-----------+----------+------------------+------------------------------------|
| DateTime  | datetime | 이벤트 일시      |                                    |
| ServerNo  | integer  | 서버 번호        | 1 이상 100 미만                    |
| MonsterCd | integer  | 몬스터 타입 코드 | 0 이상                             |
| MonsterId | integer  | 몬스터 개체 ID   | 0 이상                             |
| MapId     | integer  | 맵 번호          | 0 이상                             |
| PosX      | number   | 맵상 X 위치      |                                    |
| PosY      | number   | 맵상 Y 위치      |                                    |
| PosZ      | number   | 맵상 Z 위치      |                                    |
| ItemCd    | integer  | 아이템 타입 코드 | 1 (칼), 2 (방패), 3 (물약) 중 하나 |
| ItemId    | integer  | 아이템 개체 ID   | 0 이상                             |
| ItemName  | string   | 아이템 이름      | 7 자 이하                          |
|           |          |                  | 정규식 ^Itm.* 매칭                 |
+-----------+----------+------------------+------------------------------------+'''
    assert ans in out

    ans = '''Event : GetItem
Description : 캐릭터의 아이템 습득
+----------+----------+------------------+------------------------------------+
| Field    | Type     | Description      | Restrict                           |
|----------+----------+------------------+------------------------------------|
| DateTime | datetime | 이벤트 일시      |                                    |
| ServerNo | integer  | 서버 번호        | 1 이상 100 미만                    |
| AcntId   | integer  | 계정 ID          | 0 이상                             |
| CharId   | integer  | 캐릭터 ID        | 0 이상                             |
| MapId    | integer  | 맵 번호          | 0 이상                             |
| PosX     | number   | 맵상 X 위치      |                                    |
| PosY     | number   | 맵상 Y 위치      |                                    |
| PosZ     | number   | 맵상 Z 위치      |                                    |
| ItemCd   | integer  | 아이템 타입 코드 | 1 (칼), 2 (방패), 3 (물약) 중 하나 |
| ItemId   | integer  | 아이템 개체 ID   | 0 이상                             |
| ItemName | string   | 아이템 이름      | 7 자 이하                          |
|          |          |                  | 정규식 ^Itm.* 매칭                 |
+----------+----------+------------------+------------------------------------+'''
    assert ans in out

    res = runner.invoke(show, ['foo.lab.json', '-c', '-k'])
    assert res.exit_code == 0
    out = res.output
    ans = '''Type : types.unsigned
Description : 0 이상 정수
+------------+---------------+------------+
| BaseType   | Description   | Restrict   |
|------------+---------------+------------|
| integer    | 0 이상 정수   | 0 이상     |
+------------+---------------+------------+

Event : Login
Description : 계정 로그인
+----------+----------------+-------------------+------------------+
| Field    | Type           | Description       | Restrict         |
|----------+----------------+-------------------+------------------|
| DateTime | datetime       | 이벤트 일시       |                  |
| ServerNo | integer        | 서버 번호         | 1 이상 100 미만  |
| AcntId   | types.unsigned | 계정 ID           |                  |
| Platform | string         | 디바이스의 플랫폼 | ios, aos 중 하나 |
+----------+----------------+-------------------+------------------+
'''
    assert ans in out


def test_imp_show(clear):
    """외부 랩 파일 가져온 경우 show."""
    runner = CliRunner()

    copy_files(['boo.lab.json', 'acme2.lab.json', 'bcom.lab.json'])
    res = runner.invoke(show, ['boo.lab.json', '-k'])
    ans = '''
Domain : boo
Description : 최고의 PC 온라인 게임

Event : Login
Description : 계정 로그인
+------------+----------+---------------+-------------------------+
| Field      | Type     | Description   | Restrict                |
|------------+----------+---------------+-------------------------|
| DateTime   | datetime | 이벤트 일시   |                         |
| BcomAcntId | integer  | BCOM 계정 ID  | 0 이상                  |
| ServerNo   | integer  | 서버 번호     | 1 이상 100 미만         |
| AcntId     | integer  | 계정 ID       | 0 이상                  |
| Platform   | string   | PC의 플랫폼   | win, mac, linux 중 하나 |
+------------+----------+---------------+-------------------------+
'''
    assert ans in res.output
    res = runner.invoke(show, ['boo.lab.json', '-c', '-k'])
    assert res.exit_code == 0
    out = res.output
    ans = '''Domain : boo
Description : 최고의 PC 온라인 게임

Type : acme.types.unsigned
Description : 0 이상의 정수
+------------+---------------+------------+
| BaseType   | Description   | Restrict   |
|------------+---------------+------------|
| integer    | 0 이상의 정수 | 0 이상     |
+------------+---------------+------------+

Event : Login
Description : 계정 로그인
+------------+--------------------------+---------------+-------------------------+
| Field      | Type                     | Description   | Restrict                |
|------------+--------------------------+---------------+-------------------------|
| DateTime   | datetime                 | 이벤트 일시   |                         |
| BcomAcntId | acme.bcom.types.unsigned | BCOM 계정 ID  |                         |
| ServerNo   | integer                  | 서버 번호     | 1 이상 100 미만         |
| AcntId     | acme.types.unsigned      | 계정 ID       |                         |
| Platform   | string                   | PC의 플랫폼   | win, mac, linux 중 하나 |
+------------+--------------------------+---------------+-------------------------+
'''
    assert ans in out

    res = runner.invoke(show, ['boo.lab.json', '-c'])
    assert res.exit_code == 0
    out = res.output
    ans = '''
Type : acme.types.unsigned
Description : 0 이상의 정수
+------------+---------------+------------+
| BaseType   | Description   | Restrict   |
|------------+---------------+------------|
| integer    | 0 이상의 정수 | 0 이상     |
+------------+---------------+------------+
'''
    assert ans in out


def test_schema(clear):
    runner = CliRunner()
    copy_files(['foo.lab.json'])

    res = runner.invoke(schema, 'foo.lab.json')
    assert res.exit_code == 0
    out = res.output

    assert "foo.schema.json 에 로그 스키마 저장" in out

    # 로그 스키마 체크
    with open("foo.schema.json", 'rt', encoding='utf8') as f:
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
        'description': '아이템 타입 코드',
        'enum': [1, 2, 3]
    }
    assert defs.GetItem.properties.ItemCd == ans

    # required
    ans = ["DateTime", "ServerNo", "AcntId", "Platform"]
    assert defs.Login.required == ans
    ans = ["DateTime", "ServerNo", "AcntId"]
    assert defs.Logout.required == ans


def test_verify(clear):
    copy_files(['foo.lab.json'])

    labfile = 'foo.lab.json'
    fake_log = 'fakelog.txt'
    scmfile = 'foo.schema.json'

    args = [scmfile, fake_log]
    runner = CliRunner()
    res = runner.invoke(verify, args)
    assert res.exit_code == 2
    assert "'fakelog.txt' does not exist." in res.output

    log = '{"DateTime": "2021-08-1dd20:20:39", "Event": "Login", "ServerNo": 1, "AcntId": 1000, "Platform": "ios"}'
    write_log('fakelog.txt', log)

    res = runner.invoke(schema, [labfile])
    assert res.exit_code == 0
    res = runner.invoke(verify, args)
    assert "does not match '^([0-9]+)" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "Login", "ServerNo": 1, "AcntId": 1000}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, args)
    assert "'Platform' is a required property" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "Login", "ServerNo": 1, "AcntId": 1000, "Platform": "win"}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, args)
    assert "'win' is not one of ['ios', 'aos']" in res.output

    log = '{"DateTime": "2021-08-13T20:21:01+09:00", "Event": "Logout", "ServerNo": 1, "AcntId": -1}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, args)
    assert "-1 is less than the minimum of 0" in res.output

    log = '{"DateTime": "2021-08-13T20:21:01+09:00", "Event": "KillMonster", "ServerNo": 1, "AcntId": 1000, "CharId": 3, "MonsterCd": 3, "MonsterId": 3, "PosX": 0, "PosY": 0, "PosZ": 0}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, args)
    assert "'MapId' is a required property" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "MonsterDropItem", "ServerNo": 1, "MonsterCd": 3, "MonsterId": 3, "MapId": 1, "PosX": 0, "PosY": 0, "PosZ": 0, "ItemCd": 3, "ItemId" 4}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, args)
    assert "유효한 JSON 형식이 아닙니다" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "MonsterDropItem", "ServerNo": 1, "MonsterCd": 3, "MonsterId": 3, "MapId": 1, "PosX": 0, "PosY": 0, "PosZ": 0, "ItemCd": 3, "ItemId": 4, "ItemName": "Sword"}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, args)
    assert "'Sword' does not match '^Itm.*'" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "MonsterDropItem", "ServerNo": 1, "MonsterCd": 3, "MonsterId": 3, "MapId": 1, "PosX": 0, "PosY": 0, "PosZ": 0, "ItemCd": 100, "ItemId": 4, "ItemName": "Sword"}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, args)
    assert "100 is not one of [1, 2, 3]" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "MonsterDropItem", "ServerNo": 1, "MonsterCd": 3, "MonsterId": 3, "MapId": 1, "PosX": 0, "PosY": 0, "PosZ": 0, "ItemCd": 3, "ItemId": 4, "ItemName": "ItmSword"}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, args)
    assert "'ItmSword' is too long" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "MonsterDropItem", "ServerNo": 1, "MonsterCd": 3, "MonsterId": 3, "MapId": 1, "PosX": 0, "PosY": 0, "PosZ": 0, "ItemCd": 3, "ItemId": 4, "ItemName": "ItmSwrd"}'
    write_log('fakelog.txt', log)
    res = runner.invoke(verify, args)
    assert res.exit_code == 0


def test_imp_schema(clear):
    """외부 랩 파일 가져온 경우 schema."""
    runner = CliRunner()
    copy_files(['boo.lab.json', 'acme2.lab.json', 'bcom.lab.json'])

    res = runner.invoke(schema, ['boo.lab.json'])
    assert res.exit_code == 0
    out = res.output
    assert "boo.schema.json 에 로그 스키마 저장" in out

    # 로그 스키마 체크
    with open("boo.schema.json", 'rt', encoding='utf8') as f:
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
    ans = ['DateTime', 'BcomAcntId', 'ServerNo', 'AcntId', 'Platform']
    assert defs.Login.required == ans


def test_imp_verify(clear):
    """외부 랩 파일 가져온 경우 verify."""
    copy_files(['boo.lab.json', 'acme2.lab.json', 'bcom.lab.json'])

    fake_log = 'fakelog.txt'
    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "Login", "ServerNo": 1, "BcomAcntId": 100, "AcntId": 1000, "Platform": "ios"}'
    write_log(fake_log, log)

    runner = CliRunner()
    res = runner.invoke(schema, ['boo.lab.json'])
    assert res.exit_code == 0

    res = runner.invoke(verify, ['boo.schema.json', fake_log])
    assert res.exit_code == 1
    assert "'ios' is not one of ['win', 'mac', 'linux']" in res.output

    log = '{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "Login", "ServerNo": 1, "BcomAcntId": 100, "AcntId": 1000, "Platform": "win"}'
    write_log(fake_log, log)
    res = runner.invoke(verify, ['boo.schema.json', fake_log])
    assert res.exit_code == 0
