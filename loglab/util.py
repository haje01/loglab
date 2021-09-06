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


def fields_from_entity(root, entity, field_cb=None):
    """랩파일의 엔터티에서 필드 정보 얻기.

    Args:
        root (dict): 랩파일 데이터
        entity (dict): 엔터티 데이터
        field_cb (function): 필드값 변환 함수

    """
    fields = _init_fields()
    # mixin 이 있으면 그것의 필드를 가져옴
    if 'mixins' in entity:
        _fields = _fields_from_mixins(root, entity['mixins'])
        fields.update(_fields)
    if 'fields' in entity:
        for f in entity['fields']:
            if field_cb is not None:
                fields[f[0]] = field_cb(f[1:])
            else:
                fields[f[0]] = f[1:]
    return fields