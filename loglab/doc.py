"""메타파일에서 로그 문서 생성."""
from io import StringIO

import json
from tabulate import tabulate


def get_props_from_ebody(ebody):
    """랩파일의 이벤트 바디에서 속성들 정보 얻기."""
    return [('Datetime', 'datetime', "이벤트 일시"), ('Event', 'string', "이벤트 타입")]


def text_from_labfile(labfile_uri):
    """랩파일에서 텍스트 문서 생성."""
    with open(labfile_uri, 'rt') as f:
        body = f.read()
    data = json.loads(body)

    out = StringIO()
    headers = ['Property', 'Type', 'Description']
    for ename, ebody in data['events'].items():
        out.write('\n')
        out.write("Event : {}\n".format(ename))
        out.write("Description: {}.\n".format(ebody['desc']))
        rows = []
        props = get_props_from_ebody(ebody)
        for prop in props:
            rows.append(prop)
        out.write(tabulate(rows, headers=headers, tablefmt='psql'))
        out.write('\n')
    return out.getvalue()
