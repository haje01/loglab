"""유틸리티 모음."""
import os
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlparse
from collections import OrderedDict


LOGLAB_HOME = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()

class AttrDict(dict):
    """dict 키를 속성처럼 접근하는 헬퍼."""
    def __init__(self, *args, **kwargs):
        def from_nested_dict(data):
            """ Construct nested AttrDicts from nested dictionaries. """
            if not isinstance(data, dict):
                return data
            else:
                return AttrDict({key: from_nested_dict(data[key])
                                    for key in data})

        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

        for key in self.keys():
            self[key] = from_nested_dict(self[key])


def load_file_from(path):
    """지정된 로컬 또는 웹에서 텍스트 파일 읽기.

    Args:
        path (str): 로컬 파일 경로 또는 URI

    Returns:
        str: 읽어들인 파일 내용
    """
    parsed = urlparse(path)
    if parsed.scheme in ('http', 'https'):
        # 웹 파일
        with urlopen(path) as f:
            return f.read()
    else:
        # 로컬 파일
        with open(path, 'rt') as f:
            return f.read()


def _init_fields():
    fields = OrderedDict()
    fields["DateTime"] = ["datetime", "이벤트 일시"]
    return fields


def _fields_from_mixins(root, mixins):
    """mixins 엔터티에서 필드 정보 얻기.

    재귀적으로 올라가며 처리.

    Args:
        root (dict): 랩파일 데이터
        mixins (list): 믹스인 엔터티 이름 리스트

    Returns:
        dict: 필드 정보
    """
    fields = _init_fields()
    for mi in mixins:
        parent, entity = mi.split('.')
        _fields = fields_from_entity(root, root[parent][entity])
        fields.update(_fields)
    return fields


def _explain_rest(f):
    """제약을 설명으로 변환."""
    exps = []
    atype = f['type']
    if atype in ('integer', 'number'):
        amin = amax = xmin = xmax = None
        if 'minimum' in f:
            amin = f['minimum']
        if 'maximum' in f:
            amax = f['maximum']
        if 'exclusiveMinimum' in f:
            xmin = f['exclusiveMinimum']
        if 'exclusiveMaximum' in f:
            xmax = f['exclusiveMaximum']

        assert not(amin is not None and xmin is not None)
        assert not(amax is not None and xmax is not None)

        stmts = []
        if amin is not None:
            stmts.append(f"{amin} 이상")
        if xmin is not None:
            stmts.append(f"{xmin} 초과")
        if amax is not None:
            stmts.append(f"{amax} 이하")
        if xmax is not None:
            stmts.append(f"{xmax} 미만")
        if len(stmts) > 0:
            exps.append(' '.join(stmts))
    elif atype == 'string':
        minl = maxl = enum = ptrn = fmt = None
        if 'minLength' in f:
            minl = f['minLength']
        if 'maxLength' in f:
            maxl = f['maxLength']
        if 'enum' in f:
            enum = f['enum']
        if 'pattern' in f:
            ptrn = f['pattern']
        if 'format' in f:
            fmt = f['format']

        stmts = []
        if minl is not None:
            stmts.append(f"{minl} 자 이상")
        if maxl is not None:
            stmts.append(f"{maxl} 자 이하")
        if len(stmts) > 0:
            exps.append(' '.join(stmts))

        if enum is not None:
            exps.append(f"{enum} 중 하나")
        if ptrn is not None:
            exps.append(f"정규식 {ptrn} 매칭")
        if fmt is not None:
            exps.append(f"{fmt} 형식")
    return '\n'.join(exps)


def fields_from_entity(root, entity, field_cb=None):
    """랩파일의 엔터티에서 필드 정보 얻기.

    Args:
        root (dict): 랩파일 데이터
        entity (dict): 엔터티 데이터
        field_cb (function): 필드값 변환 함수

    """
    def _parse_field(f):
        """사전형 필드 정보 파싱."""
        opt = f['option'] if 'option' in f else None
        rest = _explain_rest(f)
        return [f['name'], f['type'], f['desc'], opt, rest]

    fields = _init_fields()
    # mixin 이 있으면 그것의 필드를 가져옴
    if 'mixins' in entity:
        _fields = _fields_from_mixins(root, entity['mixins'])
        fields.update(_fields)
    if 'fields' in entity:
        for f in entity['fields']:
            # 사전형 필드 정보 파싱
            if type(f) is dict:
                f = _parse_field(f)
            if field_cb is not None:
                fields[f[0]] = field_cb(f[1:])
            else:
                fields[f[0]] = f[1:]
    return fields
