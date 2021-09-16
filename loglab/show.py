"""랩 파일에서 출력용 문서 생성."""
from io import StringIO

import pandas as pd
from tabulate import tabulate

from loglab.util import fields_from_entity, explain_rstr


def _jsonify(vals):
    """문서 출력을 위해 파이썬 값을 JSON 형태로."""
    _vals = []
    for val in vals:
        if type(val) is bool:
            _vals.append(str(val).lower())
        else:
            _vals.append(val)
    return _vals


def text_from_labfile(root, out=None, ns=None):
    """랩 파일에서 텍스트 문서 생성.

    Args:
        root (dict): 랩 파일 데이터
        out (StringIO): 문자열 IO
        ns (string): 네임스페이스

    """
    if out is None:
        out = StringIO()

    # 가져온 랩 파일 먼저
    if '_extern_' in root:
        for k, v in root['_extern_'].items():
            text_from_labfile(v, out, k)

    nsp = '' if ns is None else f'{ns}.'

    # 도메인
    if 'domain' in root:
        out.write('\n')
        out.write(f"Domain : {root['domain']['name']}\n")
        if 'desc' in root['domain']:
            out.write("Description : {}\n".format(root['domain']['desc']))

    # 커스텀 타입
    if 'types' in root:
        out.write('\n')
        for tname, tdef in root['types'].items():
            out.write(f"Type : {nsp}types.{tname}\n")
            out.write(f"Description : {tdef['desc']}\n")
            rstr = explain_rstr(tdef)
            df = pd.DataFrame(dict(BaseType=[tdef['type']],
                              Description=[tdef['desc']],
                              Restrict=[rstr]))
            df = df.set_index('BaseType')
            tbl = tabulate(df, headers=df.reset_index().columns, tablefmt='psql')
            out.write(tbl)
            out.write('\n')

    if 'events' not in root:
        return out.getvalue()

    headers = ['Field', 'Type', 'Description', 'Optional', 'Restrict']
    # 각 이벤트별로
    for ename, ebody in root['events'].items():
        out.write('\n')
        out.write(f"Event : {nsp}{ename}\n")
        out.write(f"Description : {ebody['desc']}\n")

        rows = []
        fields = fields_from_entity(root, ebody, field_cb=_jsonify)
        max_col = 0
        for k, v in fields.items():
            # restrict 제거
            if len(v) >= 5:
                v = v[:4]
            if max_col < len(v) + 1:
                max_col = len(v) + 1
            rows.append([k] + v)
        df = pd.DataFrame(rows, columns=headers[:max_col]).set_index('Field')
        df = df.dropna(how='all', axis=1)
        tbl = tabulate(df, headers=df.reset_index().columns, tablefmt='psql')
        out.write(tbl)
        out.write('\n')
    return out.getvalue()
