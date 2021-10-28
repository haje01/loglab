import pytest
import copy

from loglab.model import _build_domain, _build_types, _build_bases,\
    _build_events, build_model, _handle_import


def test_domain():
    data = {
        "domain": {
            "name": "bcom",
            "desc": "위대한 회사"
        }
    }
    domain = _build_domain(data)
    assert domain['name'] == 'bcom'
    assert domain['desc'] == "위대한 회사"


def test_types():
    data1 = {
        "domain": {
            "name": "bcom",
            "desc": "위대한 회사"
        },
        "types": {
            "Id": {
                "type": "integer",
                "desc": "Id 타입",
                "minimum": 0
            }
        }
    }
    types = _build_types(data1)
    assert {
        'Id': [
            [
            "",
            {
                "type": "integer",
                "desc": "Id 타입",
                "minimum": 0
            }
            ]
        ]
    } == types

    data2 = {
        "domain": {
            "name": "acme",
            "desc": "위대한 게임 회사"
        },
        "_imported_": [data1]
    }
    types = _build_types(data2)
    assert {
        'Id': [
            ['bcom',
            {
                'type': 'integer',
                'desc': 'Id 타입',
                'minimum': 0
            }
            ]
        ]
        } == types

    data3 = {
        "domain": {
            "name": "foo",
            "desc": "위대한 게임"
        },
        "_imported_": [data2],
    }
    types = _build_types(data3)
    assert {
        'Id': [
            [
            "acme.bcom",
            {
                "type": "integer",
                "desc": "Id 타입",
                "minimum": 0
            }
            ]
        ]
    } == types


def test_mixins():
    data1 = {
        "domain": {
            "name": "foo",
            "desc": "위대한 게임"
        },
        "bases": {
            "Account": {
                "desc": "계정 정보",
                "fields": [
                    ["AcntId", "integer", "계정 ID"]
                ]
            },
            "Character": {
                "desc": "캐릭터 정보",
                "mixins": ["bases.Account"],
                "fields": [
                    ["CharId", "integer", "계정 ID"]
                ]
            }
        }
    }
    bases = _build_bases(data1, None)
    assert {'Account': [
            ['',
            {
                'desc': '계정 정보',
                'fields': {
                    'AcntId': [
                        ['',
                        {
                            'type': 'integer',
                            'desc': '계정 ID'
                        }
                        ]
                    ]
                }
            }
            ]
        ],
        'Character': [
        ['',
        {
            'desc': '캐릭터 정보',
            'fields': {
                'AcntId': [
                    ['',
                    {
                        'type': 'integer',
                        'desc': '계정 ID'
                    }
                    ]
                ],
                'CharId': [
                    ['',
                    {
                        'type': 'integer',
                        'desc': '계정 ID'
                    }
                    ]
                ]
            }
        }
        ]
    ]
} == bases


def test_bases():
    data1 = {
        "domain": {
            "name": "bcom",
            "desc": "위대한 회사"
        },
        "types": {
            "Id": {
                "type": "integer",
                "desc": "Id 타입",
                "minimum": 0
            }
        },
        "bases": {
            "Account": {
                "desc": "BCOM 계정 정보",
                "fields": [
                    ["BcomAcntId", "types.Id", "BCOM 계정 ID"]
                ]
            },
        }
    }
    _data1 = copy.deepcopy(data1)
    bases = _build_bases(data1, None)
    assert _data1 == data1
    assert {
        "Account": [
            [
                "",
                {
                    "desc": "BCOM 계정 정보",
                    "fields": {
                        "BcomAcntId": [
                            [
                                "",
                                {
                                   'type': 'integer',
                                   'desc': 'BCOM 계정 ID', 'minimum': 0
                                }
                            ]
                        ]
                    }
                }
            ]
        ]
    } == bases

    data2 = {
        "domain": {
            "name": "acme",
            "desc": "위대한 게임 회사"
        },
        "_imported_": [data1],
        "bases": {
            "Account": {
                "desc": "ACME 계정 정보",
                "mixins": ["bcom.bases.Account"],
                "fields": [
                    ["AcmeAcntId", "bcom.types.Id", "ACME 계정 ID"]
                ]
            }
        }
    }
    _data2 = copy.deepcopy(data2)
    bases = _build_bases(data2, None)
    assert _data2 == data2
    assert {
        "Account": [
            [
                'bcom',
                {
                    'desc': 'BCOM 계정 정보',
                    'fields': {
                        'BcomAcntId': [
                            [
                                'bcom', {
                                    "type": "integer",
                                    "minimum": 0,
                                    'desc': 'BCOM 계정 ID'
                                }
                            ]
                        ]
                    }
                }
            ],
            [
                "",
                {
                    "desc": "ACME 계정 정보",
                    "fields": {
                        "BcomAcntId": [
                            [
                                "bcom",
                                {
                                    "type": "integer",
                                    "minimum": 0,
                                    "desc": "BCOM 계정 ID"
                                }
                            ]
                        ],
                        "AcmeAcntId": [
                            [
                                "",
                                {
                                    "type": "integer",
                                    "minimum": 0,
                                    "desc": "ACME 계정 ID"
                                }
                            ]
                        ]
                    }
                }
            ]
        ]
    } == bases

    data3 = {
        "domain": {
            "name": "foo",
            "desc": "위대한 게임"
        },
        "_imported_": [data2],
        "bases": {
            "Character": {
                "desc": "FOO 캐릭터 정보",
                "fields": [
                    ["CharId", "acme.types.Id", "캐릭터 ID"]
                ]
            }
        },
        "events": {
            "CharLogin": {
                "desc": "FOO 캐릭터 로그인",
                "mixins": ["acme.bases.Account", "bases.Character"]
            }
        }
    }
    _data3 = copy.deepcopy(data3)
    bases = _build_bases(data3, None)
    assert _data3 == data3
    assert {
        'Account': [
            ['acme.bcom', {
                'desc': 'BCOM 계정 정보',
                'fields': {
                    'BcomAcntId': [
                        ['acme.bcom',
                        {
                            'type': 'integer',
                            'desc': 'BCOM 계정 ID',
                            'minimum': 0
                        }
                        ]
                    ]
                    }
                }
            ],
            ['acme', {
                'desc': 'ACME 계정 정보',
                'fields': {
                    'BcomAcntId': [
                        ['acme.bcom',
                        {
                            'type': 'integer',
                            'desc': 'BCOM 계정 ID',
                            'minimum': 0
                        }
                        ]
                    ],
                    'AcmeAcntId': [
                        ['acme',
                        {
                            'type': 'integer',
                            'desc': 'ACME 계정 ID',
                            'minimum': 0
                        }
                        ]
                    ]
                    }
                }
            ]
        ],
        'Character': [
            ['',
            {
                'desc': 'FOO 캐릭터 정보',
                'fields': {
                    'CharId': [
                        ['',
                        {
                            'type': 'integer',
                            'desc': '캐릭터 ID',
                            'minimum': 0
                        }
                        ]
                    ]
                }
            }
            ]
        ]
    } == bases


def test_bases2():
    data = {
        "domain": {
            "name": "bcom",
            "desc": "위대한 회사"
        },
        "types": {
            "Id": {
                "type": "integer",
                "desc": "Id 타입",
                "minimum": 0
            }
        },
        "bases": {
            "Server": {
                "desc": "서버 정보",
                "fields": [
                    {
                        "name": "ServerNo",
                        "desc": "서버 번호",
                        "type": "integer",
                        "option": True,
                        "minimum": 1,
                        "exclusiveMaximum": 100
                    }
                ]
            }
        }
    }
    bases = _build_bases(data, None)
    assert {
        'Server': [
            ['',
            {
                'desc': '서버 정보',
                'fields': {
                    'ServerNo': [
                        ['',
                        {
                            'type': 'integer',
                            'desc': '서버 번호',
                            "option": True,
                            'minimum': 1,
                            'exclusiveMaximum': 100
                        }
                        ]
                    ]
                }
            }
            ]
        ]} == bases


def test_events():
    data = {
        "domain": {
            "name": "bcom",
            "desc": "위대한 회사"
        },
        "types": {
            "Id": {
                "type": "integer",
                "desc": "Id 타입",
                "minimum": 0
            }
        },
        "bases": {
            "Account": {
                "desc": "계정 정보",
                "fields": [
                    ["AcntId", "types.Id", "계정 ID"]
                ]
            }
        },
        "events": {
            "Logout": {
                "desc": "계정 로그아웃",
                "mixins": ["bases.Account"],
                "fields": [
                    ["PlayTime", "number", "플레이 시간 (초)", True]
                ]
            }
        }
    }
    events = _build_events(data)
    assert {
        'Logout': [
            ['',
            {
                'desc': '계정 로그아웃',
                'fields': {
                    'DateTime': [
                        ['',
                        {
                            'type': 'datetime',
                            'desc': '이벤트 일시'
                        }
                        ]
                    ],
                    'AcntId': [
                        ['',
                        {
                            'type': 'integer',
                            'desc': '계정 ID',
                            'minimum': 0
                        }
                        ]
                    ],
                    'PlayTime': [
                        ['',
                        {
                            'type': 'number',
                            'desc': '플레이 시간 (초)',
                            'option': True
                        }
                        ]
                    ]
                }
            }
            ]
        ]
    } == events

    data = {
        "domain": {
            "name": "bcom",
            "desc": "위대한 회사"
        },
        "types": {
            "Id": {
                "type": "integer",
                "desc": "Id 타입",
                "minimum": 0
            }
        },
        "bases": {
            "Account": {
                "desc": "계정 정보",
                "fields": [
                    ["AcntId", "types.Id", "계정 ID"]
                ]
            }
        },
        "events": {
            "Logout": {
                "desc": "계정 로그아웃",
                "mixins": ["bases.Account"],
                "fields": [
                    {
                        "name": "PlayTime",
                        "type": "number",
                        "desc": "플레이 시간 (초)",
                        "option": True
                    }
                ]
            }
        }
    }
    events = _build_events(data)
    assert {
        'Logout': [
            ['',
            {
                'desc': '계정 로그아웃',
                'fields': {
                    'DateTime': [
                        ['',
                        {
                            'type': 'datetime',
                            'desc': '이벤트 일시'
                        }
                        ]
                    ],
                    'AcntId': [
                        ['',
                        {
                            'type': 'integer',
                            'desc': '계정 ID',
                            'minimum': 0
                        }
                        ]
                    ],
                    'PlayTime': [
                        ['',
                        {
                            'type': 'number',
                            'desc': '플레이 시간 (초)',
                            'option': True
                        }
                        ]
                    ]
                }
            }
            ]
        ]
    } == events

    data1 = {
        "domain": {
            "name": "bcom",
            "desc": "위대한 회사"
        },
        "types": {
            "Id": {
                "type": "integer",
                "desc": "Id 타입",
                "minimum": 0
            }
        },
        "bases": {
            "Account": {
                "desc": "BCOM 계정 정보",
                "fields": [
                    ["BcomAcntId", "types.Id", "BCOM 계정 ID"]
                ]
            },
        }
    }
    data2 = {
        "domain": {
            "name": "acme",
            "desc": "위대한 게임 회사"
        },
        "_imported_": [data1],
        "bases": {
            "Account": {
                "desc": "ACME 계정 정보",
                "mixins": ["bcom.bases.Account"],
                "fields": [
                    ["AcmeAcntId", "bcom.types.Id", "ACME 계정 ID"]
                ]
            }
        },
        "events": {
            "AcntLogin": {
                "desc": "ACME 계정 로그인",
                "mixins": ["bases.Account"]
            }
        }
    }
    _data2 = copy.deepcopy(data2)
    events = _build_events(data2)
    assert _data2 == data2
    assert {
        'AcntLogin': [
            [
                '',
                {
                'desc': 'ACME 계정 로그인',
                'fields': {
                    'DateTime': [
                        ['',
                        {
                            'type': 'datetime',
                            'desc': '이벤트 일시'
                        }
                        ]
                    ],
                    'BcomAcntId': [
                        ['bcom',
                        {
                            'type': 'integer',
                            'desc': 'BCOM 계정 ID',
                            'minimum': 0
                        }
                        ]
                    ],
                    'AcmeAcntId': [
                        ['',
                        {
                            'type': 'integer',
                            'desc': 'ACME 계정 ID',
                            'minimum': 0
                        }
                        ]
                    ]
                    }
                }
            ]
        ]
    } == events

    data3 = {
        "domain": {
            "name": "foo",
            "desc": "위대한 게임"
        },
        "_imported_": [data2],
        "bases": {
            "Character": {
                "desc": "FOO 캐릭터 정보",
                "fields": [
                    ["CharId", "acme.types.Id", "캐릭터 ID"]
                ]
            }
        },
        "events": {
            "CharLogin": {
                "desc": "FOO 캐릭터 로그인",
                "mixins": ["acme.bases.Account", "bases.Character"]
            }
        }
    }
    events = _build_events(data3)
    assert {
        'AcntLogin': [
            [
                'acme',
                {
                'desc': 'ACME 계정 로그인',
                'fields': {
                    'DateTime': [
                        ['',
                        {
                            'type': 'datetime',
                            'desc': '이벤트 일시'
                        }
                        ]
                    ],
                    'BcomAcntId': [
                        ['acme.bcom',
                        {
                            'type': 'integer',
                            'desc': 'BCOM 계정 ID',
                            'minimum': 0
                        }
                        ]
                    ],
                    'AcmeAcntId': [
                        ['acme',
                        {
                            'type': 'integer',
                            'desc': 'ACME 계정 ID',
                            'minimum': 0
                        }
                        ]
                    ]
                    }
                }
            ]
        ],
        'CharLogin': [
            ['',
            {
                'desc': 'FOO 캐릭터 로그인',
                'fields': {
                    'DateTime': [
                        ['',
                        {
                            'type': 'datetime',
                            'desc': '이벤트 일시'
                        }
                        ]
                    ],
                    'BcomAcntId': [
                        ['acme.bcom',
                        {
                            'type': 'integer',
                            'desc': 'BCOM 계정 ID',
                            'minimum': 0
                        }
                        ]
                    ],
                    'AcmeAcntId': [
                        ['acme',
                        {
                            'type': 'integer',
                            'desc': 'ACME 계정 ID',
                            'minimum': 0
                        }
                        ]
                    ],
                    'CharId': [
                        ['',
                        {
                            'type': 'integer',
                            'desc': '캐릭터 ID',
                            'minimum': 0
                        }
                        ]
                    ]
                }
            }
            ]
        ]
    } == events


def test_excpt():
    data = {
        "domain": {
            "name": "bcom",
            "desc": "위대한 회사"
        },
        "types": {
            "Id": {
                "type": "integer",
                "desc": "Id 타입",
                "minimum": 0
            }
        },
        "bases": {
            "Account": {
                "desc": "BCOM 계정 정보",
                "fields": [
                    ["BcomAcntId", "types.Id", "BCOM 계정 ID"]
                ]
            },
        },
        "events": {
            "Account": {
                "desc": "BCOM 계정 정보",
                "fields": [
                    ["BcomAcntId", "types.Id", "BCOM 계정 ID"]
                ]
            }
        }
    }

    data = {
        "domain": {
            "name": "bcom",
            "desc": "위대한 회사"
        },
        "types": {
            "Id": {
                "type": "integer",
                "desc": "Id 타입",
                "minimum": 0
            }
        },
        "bases": {
            "Account": {
                "desc": "BCOM 계정 정보",
                "mixins": ["asdf"],
                "fields": [
                    ["BcomAcntId", "types.Id", "BCOM 계정 ID"]
                ]
            },
        }
    }
    with pytest.raises(Exception, match='Illegal mixin path'):
        _build_events(data)

    data = {
        "domain": {
            "name": "bcom",
            "desc": "위대한 회사"
        },
        "types": {
            "Id": {
                "type": "integer",
                "desc": "Id 타입",
                "minimum": 0
            }
        },
        "bases": {
            "Account": {
                "desc": "BCOM 계정 정보",
                "mixins": ["asdf.asdf"],
                "fields": [
                    ["BcomAcntId", "types.Id", "BCOM 계정 ID"]
                ]
            },
        }
    }
    with pytest.raises(Exception, match='Illegal mixin type'):
        _build_events(data)

    data = {
        "domain": {
            "name": "bcom",
            "desc": "위대한 회사"
        },
        "types": {
            "Id": {
                "type": "integer",
                "desc": "Id 타입",
                "minimum": 0
            }
        },
        "bases": {
            "Account": {
                "desc": "BCOM 계정 정보",
                "mixins": ["bases.asdf"],
                "fields": [
                    ["BcomAcntId", "types.Id", "BCOM 계정 ID"]
                ]
            },
        }
    }
    with pytest.raises(Exception, match="not find mixin 'asdf' in bases"):
        _build_events(data)


def test_desc():
    acme = {
        "domain": {
            "name": "acme",
            "desc": "최고의 게임 회사"
        },
        "events": {
            "Login": {
            }
        }
    }
    boo = {
        "domain": {
            "name": "boo",
            "desc": "최고의 PC 온라인 게임"
        },
        "import": [acme],
        "events": {
            "Login": {
                "mixins": ["acme.events.Login"],
            }
        }
    }
    with pytest.raises(Exception, match='Can not resolve description'):
        _handle_import(boo)
        boo = build_model(boo)

    acme = {
        "domain": {
            "name": "acme",
            "desc": "최고의 게임 회사"
        },
        "events": {
            "Login": {
                "desc": "ACME 계정 로그인",
            }
        }
    }
    boo = {
        "domain": {
            "name": "boo",
            "desc": "최고의 PC 온라인 게임"
        },
        "import": [acme],
        "events": {
            "Login": {
                "mixins": ["acme.events.Login"],
            }
        }
    }
    _handle_import(boo)
    boo = build_model(boo)
    assert boo.events.Login[-1][1]['desc'] == 'ACME 계정 로그인'

    bcom = {
        "domain": {
            "name": "bcom",
            "desc": "최고의 회사"
        },
        "events": {
            "Login": {
                "desc": "BCOM 계정 로그인",
            }
        }
    }
    acme = {
        "domain": {
            "name": "acme",
            "desc": "최고의 게임 회사"
        },
        "import": [bcom],
        "events": {
            "Login": {
                "mixins": ["bcom.events.Login"],
            }
        }
    }
    boo = {
        "domain": {
            "name": "boo",
            "desc": "최고의 PC 온라인 게임"
        },
        "import": [acme],
        "events": {
            "Login": {
                "mixins": ["acme.events.Login"],
            }
        }
    }
    _handle_import(boo)
    boo = build_model(boo)
    assert boo.events.Login[-1][1]['desc'] == 'BCOM 계정 로그인'

    acme = {
        "domain": {
            "name": "acme",
            "desc": "최고의 게임 회사"
        },
        "events": {
            "Login": {
            }
        }
    }
    boo = {
        "domain": {
            "name": "boo",
            "desc": "최고의 PC 온라인 게임"
        },
        "import": [acme],
        "bases": {
            "Server": {
                "desc": "서버 정보",
                "fields": [
                    ["ServerNo", "integer", "서버 번호"]
                ]
            },
            "Account": {
                "desc": "계정 정보",
                "fields": [
                    ["AcntId", "integer", "계정 번호"]
                ]
            }
        },
        "events": {
            "Login": {
                "mixins": ["acme.events.Login", "bases.Server", "bases.Account"]
            }
        }
    }
    _handle_import(boo)
    boo = build_model(boo)
    assert boo.events.Login[-1][1]['desc'] == '서버 정보'


def test_multi_imp():
    acme = {
        "domain": {
            "name": "acme",
            "desc": "최고의 게임 회사"
        },
        "events": {
            "Login": {
                "desc": "ACME 로그인",
            }
        }
    }
    payme = {
        "domain": {
            "name": "payme",
            "desc": "최고의 결제 회사"
        },
        "events": {
            "Charge": {
                "desc": "PAYME 충전"
            }
        }
    }
    boo = {
        "domain": {
            "name": "boo",
            "desc": "최고의 PC 온라인 게임"
        },
        "import": [acme, payme],
        "events": {
            "Login": {
                "mixins": ["acme.events.Login"],
            },
            "Charge": {
                "mixins": ["payme.events.Charge"],
            }
        }
    }
    _handle_import(boo)
    boo = build_model(boo)
    assert 'Login' in boo['events'].keys()
    assert 'Charge' in boo['events'].keys()