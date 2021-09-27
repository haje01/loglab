import pandas as pd
import pytest
import copy

from loglab.util import test_reset
from loglab.dom import _build_types, _build_bases, _build_events


@pytest.fixture
def clear():
    test_reset


def test_types(clear):
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
        "import": [data1]
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
        "import": [data2],
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


def test_mixins(clear):
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
    bases = _build_bases(data1)
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


def test_bases(clear):
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
    bases = _build_bases(data1)
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
        "import": [data1],
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
    bases = _build_bases(data2)
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
        "import": [data2],
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
    bases = _build_bases(data3)
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


def test_events(clear):
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
        "import": [data1],
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
    # _data2 = copy.deepcopy(data2)
    # events = _build_events(data2)
    # assert _data2 == data2
    # assert {
    #     'AcntLogin': [
    #         [
    #             '',
    #             {
    #             'desc': 'ACME 계정 로그인',
    #             'fields': {
    #                 'BcomAcntId': [
    #                     ['bcom',
    #                     {
    #                         'type': 'integer',
    #                         'desc': 'BCOM 계정 ID',
    #                         'minimum': 0
    #                     }
    #                     ]
    #                 ],
    #                 'AcmeAcntId': [
    #                     ['',
    #                     {
    #                         'type': 'integer',
    #                         'desc': 'ACME 계정 ID',
    #                         'minimum': 0
    #                     }
    #                     ]
    #                 ]
    #                 }
    #             }
    #         ]
    #     ]
    # } == events

    data3 = {
        "domain": {
            "name": "foo",
            "desc": "위대한 게임"
        },
        "import": [data2],
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
