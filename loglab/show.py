"""랩 파일에서 출력용 문서 생성."""
from io import StringIO

import pandas as pd
from tabulate import tabulate
from jinja2 import Environment, FileSystemLoader

from loglab.dom import build_dom
from loglab.util import explain_rstr, LOGLAB_HOME


def _jsonify(vals):
    """문서 출력을 위해 파이썬 값을 JSON 형태로."""
    _vals = []
    for val in vals:
        if type(val) is bool:
            _vals.append(str(val).lower())
        else:
            _vals.append(val)
    return _vals


def _get_dmp(domain):
    return f'{domain}.' if len(domain) > 0 else ''


def _write_custom_types(dom, out):
    out.write('\n')
    for tname, tlst in dom['types'].items():
        td = tlst[-1]
        dmp = _get_dmp(td[0])
        tdef = td[1]
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


def _write_events(name, data, out):
    headers = ['Field', 'Type', 'Description', 'Optional', 'Restrict']

    out.write('\n')
    dmp = _get_dmp(data[0])
    edef = data[1]
    out.write(f"Event : {dmp}{name}\n")
    out.write(f"Description : {edef['desc']}\n")

    rows = []
    for k, v in edef['fields'].items():
        fdata = v[-1]
        dmp = _get_dmp(fdata[0])
        fdef = fdata[1]
        rstr = explain_rstr(fdef)
        opt = fdef['option'] if 'option' in fdef else None
        rows.append([k, fdef['type'], fdef['desc'], opt, rstr])
    df = pd.DataFrame(rows, columns=headers).set_index('Field')
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

    dom = build_dom(root)

    # 도메인
    out.write('\n')
    out.write(f"Domain : {dom['domain']['name']}\n")
    if 'desc' in dom['domain']:
        out.write("Description : {}\n".format(dom['domain']['desc']))

    # 커스텀 타입
    if 'types' in root:
        _write_custom_types(dom, out)

    # 각 이벤트별로
    for ename, elst in dom['events'].items():
        edata = elst[-1]
        _write_events(ename, edata, out)

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
