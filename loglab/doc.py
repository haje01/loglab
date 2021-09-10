"""메타파일에서 로그 문서 생성."""
from io import StringIO
import json

import pandas as pd
from tabulate import tabulate

from loglab.util import fields_from_entity


def _jsonify(vals):
    """문서 출력을 위해 파이썬 값을 JSON 형태로."""
    _vals = []
    for val in vals:
        if type(val) is bool:
            _vals.append(str(val).lower())
        else:
            _vals.append(val)
    return _vals


def text_from_labfile(root):
    """랩파일에서 텍스트 문서 생성.

    Args:
        root (dict): 랩파일 데이터

    """
    out = StringIO()

    # 도메인
    if 'domain' in root:
        out.write('\n')
        out.write("Domain : {}\n".format(root['domain']['name']))
        if 'desc' in root['domain']:
            out.write("Description : {}\n".format(root['domain']['desc']))

    headers = ['Field', 'Type', 'Description', 'Optional', 'Restrict']
    # 각 이벤트별로
    for ename, ebody in root['events'].items():
        out.write('\n')
        out.write("Event : {}\n".format(ename))
        out.write("Description : {}\n".format(ebody['desc']))

        rows = []
        fields = fields_from_entity(root, ebody, field_cb=_jsonify)
        max_col = 0
        for k, v in fields.items():
            if max_col < len(v) + 1:
                max_col = len(v) + 1
            rows.append([k] + v)
        df = pd.DataFrame(rows, columns=headers[:max_col]).set_index('Field')
        df = df.dropna(how='all', axis=1)
        tbl = tabulate(df, headers=df.reset_index().columns, tablefmt='psql')
        out.write(tbl)
        out.write('\n')
    return out.getvalue()
