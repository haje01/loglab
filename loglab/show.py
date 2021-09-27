"""랩 파일에서 출력용 문서 생성."""
from io import StringIO

import pandas as pd
from tabulate import tabulate
from jinja2 import Environment, FileSystemLoader

from loglab.util import fields_from_entity, explain_rstr, LOGLAB_HOME


def _jsonify(vals):
    """문서 출력을 위해 파이썬 값을 JSON 형태로."""
    _vals = []
    for val in vals:
        if type(val) is bool:
            _vals.append(str(val).lower())
        else:
            _vals.append(val)
    return _vals


def _write_custom_types(root, out, dmp, host):
    out.write('\n')
    for tname, tdef in root['types'].items():
        # 호스트에서 재정의된 타입은 출력 않음
        if host is not None and 'types' in host:
            if tname in host['types']:
                continue
        out.write(f"Type : {dmp}types.{tname}\n")
        out.write(f"Description : {tdef['desc']}\n")
        rstr = explain_rstr(tdef)
        df = pd.DataFrame(dict(BaseType=[tdef['type']],
                               Description=[tdef['desc']],
                               Restrict=[rstr]))
        df = df.set_index('BaseType')
        tbl = tabulate(df, headers=df.reset_index().columns, tablefmt='psql')
        out.write(tbl)
        out.write('\n')


def _write_events(root, out, domain, prefix_dm, dmp, ename, ebody, host):
    headers = ['Field', 'Type', 'Description', 'Optional', 'Restrict']

    out.write('\n')
    out.write(f"Event : {dmp}{ename}\n")
    out.write(f"Description : {ebody['desc']}\n")

    rows = []
    fields = fields_from_entity(root, ebody, domain, prefix_dm, field_cb=_jsonify)
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


def text_from_labfile(root, out=None, domain=None, prefix_dm=False, host=None):
    """랩 파일에서 텍스트 문서 생성.

    Args:
        root (dict): 랩 데이터
        out (StringIO): 문자열 IO
        domain (string): 도메인 이름
        prefix_dm (bool): 요소 이름에 도메인 접두어 여부
        host (dict): 이 랩을 불러온 랩 데이터

    """
    if out is None:
        out = StringIO()

    # 가져온 랩 파일 먼저
    if '_extern_' in root:
        for k, v in root['_extern_'].items():
            text_from_labfile(v, out, k, prefix_dm=prefix_dm,
                              host=root)

    dmp = ''
    if domain is not None and prefix_dm:
        dmp = f'{domain}.'

    # 도메인
    if 'domain' in root:
        out.write('\n')
        out.write(f"Domain : {root['domain']['name']}\n")
        if 'desc' in root['domain']:
            out.write("Description : {}\n".format(root['domain']['desc']))

    # 커스텀 타입
    if 'types' in root:
        _write_custom_types(root, out, prefix_dm, dmp, host)

    if 'events' not in root:
        return out.getvalue()

    # 각 이벤트별로
    for ename, ebody in root['events'].items():
        # 호스트에서 재정의된 이벤트는 출력 않음
        if host is not None and 'events' in host:
            if ename in host['events']:
                continue
        _write_events(root, out, domain, prefix_dm, dmp, ename, ebody, host)

    return out.getvalue()


def html_from_labfile(root, out=None, ns=None):
    """랩 파일에서 HTML 파일 생성.

    Args:
        root (dict): 랩 파일 데이터
        out (StringIO): 문자열 IO
        domain (string): 도메인 이름

    """
    tmpl_path = os.path.join(LOGLAB_HOME, "template")
    loader = FileSystemLoader(tmpl_path)
    env = Environment(loader=loader)
    tmpl = env.get_template("tmpl_doc.html")
    return tmpl.render(labfile=labfile, events=events, fields=fields)
