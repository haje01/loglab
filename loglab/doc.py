"""메타파일에서 로그 문서 생성."""
from io import StringIO

import json
from tabulate import tabulate


def get_props_from_ebody(ebody):
    """메타파일의 이벤트 바디에서 속성들 정보 얻기."""
    return [('datetime', 'datetime'), ('event', 'string')]


def text_from_meta(meta_path):
    """메타파일에서 텍스트 문서 생성."""
    with open(meta_path, 'rt') as f:
        body = f.read()
    data = json.loads(body)

    out = StringIO()
    headers = ['Property', 'Type']
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
