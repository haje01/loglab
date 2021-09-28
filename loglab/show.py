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


def _write_custom_types(dom, out, namef):
    # 출력할 것이 있는지 확인
    cnt = 0
    for tname, tlst in dom['types'].items():
        td = tlst[-1]
        dmp = _get_dmp(td[0])
        qtname = f'{dmp}types.{tname}'
        if namef is None or namef.search(qtname) is not None:
            cnt += 1
    if cnt > 0:
        out.write('\n')

    for tname, tlst in dom['types'].items():
        td = tlst[-1]
        dmp = _get_dmp(td[0])
        tdef = td[1]
        qtname = f'{dmp}types.{tname}'
        if namef is not None and namef.search(qtname) is None:
            continue

        out.write(f"Type : {qtname}\n")
        out.write(f"Description : {tdef['desc']}\n")
        rstr = explain_rstr(tdef)
        df = pd.DataFrame(dict(BaseType=[tdef['type']],
                               Description=[tdef['desc']],
                               Restrict=[rstr]))
        df = df.set_index('BaseType')
        tbl = tabulate(df, headers=df.reset_index().columns, tablefmt='psql')
        out.write(tbl)
        out.write('\n')


def _write_events(name, data, out, namef):
    headers = ['Field', 'Type', 'Description', 'Optional', 'Restrict']

    dmp = _get_dmp(data[0])
    edef = data[1]
    qname = f'{dmp}{name}'
    if namef is not None and namef.search(qname) is None:
        return

    out.write('\n')
    out.write(f"Event : {qname}\n")
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


def text_from_labfile(data, cus_type, namef, out=None, domain=None,
                      host=None):
    """랩 파일에서 텍스트 문서 생성.

    Args:
        data (dict): 랩 데이터
        cus_type (bool): 커스텀 타입 출력 여부. 기본 False
        namef (str): 이름 필터
        out (StringIO): 문자열 IO
        domain (string): 도메인 이름
        host (dict): 이 랩을 불러온 랩 데이터

    """
    if out is None:
        out = StringIO()

    dom = build_dom(data, cus_type)

    # 도메인
    out.write('\n')
    out.write(f"Domain : {dom.domain.name}\n")
    if 'desc' in dom.domain:
        out.write("Description : {}\n".format(dom.domain.desc))

    # 커스텀 타입
    if 'types' in dom and cus_type:
        _write_custom_types(dom, out, namef)

    # 각 이벤트별로
    for ename, elst in dom.events.items():
        edata = elst[-1]
        _write_events(ename, edata, out, namef)

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
