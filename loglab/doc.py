"""메타파일에서 로그 문서 생성."""
from io import StringIO
import json
from collections import OrderedDict

from tabulate import tabulate


def get_fields_from_mixins(root, mixins):
    """mixins 엔터티에서 필드 정보 얻기.

    Args:
        root (dict): 랩파일 데이터
        mixins (list): 믹스인 엔터티 이름 리스트

    Returns:
        dict: 필드 정보
    """
    fields = []
    for mi in mixins:
        parent, entity = mi.split('.')
        _fields = get_fields_from_entity(root, root[parent][entity])
        fields += _fields
    return fields


def get_fields_from_entity(root, entity):
    """랩파일의 엔터티에서 필드 정보 얻기.

    Args:
        root (dict): 랩파일 데이터
        entity (dict): 엔터티 데이터

    """
    fields = []
    # mixin 이 있으면 그것의 필드를 가져옴
    if 'mixins' in entity:
        _fields = get_fields_from_mixins(root, entity['mixins'])
        fields += _fields
    if 'fields' in entity:
        fields += entity['fields']
    return fields


def text_from_labfile(root):
    """랩파일에서 텍스트 문서 생성.

    Args:
        root (dict): 랩파일 데이터

    """
    out = StringIO()
    headers = ['Property', 'Type', 'Description']
    # 각 이벤트별로
    for ename, ebody in root['events'].items():
        out.write('\n')
        out.write("Event : {}\n".format(ename))
        out.write("Description: {}\n".format(ebody['desc']))
        rows = []
        fields = get_fields_from_entity(root, ebody)
        for field in fields:
            rows.append(field)
        out.write(tabulate(rows, headers=headers, tablefmt='psql'))
        out.write('\n')
    return out.getvalue()
