"""랩 파일에서 출력용 문서 생성."""
import os
from io import StringIO

from tabulate import tabulate
from jinja2 import Environment, FileSystemLoader

from loglab.dom import build_dom
from loglab.util import explain_rstr, LOGLAB_HOME, absdir_for_html


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


def _write_type_table(tdef, out):
    headers = ['BaseType', 'Description']
    row = [tdef['type'], tdef['desc']]
    rstr = explain_rstr(tdef)
    if rstr != '':
        headers.append('Restrict')
        row.append(rstr)
    tbl = tabulate([row], headers, tablefmt='psql')
    out.write(tbl)
    out.write('\n')


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
        _write_type_table(tdef, out)


def _write_table(edef, out):
    headers = ['Field', 'Type', 'Description']
    fields = []
    types = []
    descs = []
    opts = []
    rstrs = []
    for k, v in edef['fields'].items():
        fdata = v[-1]
        fdef = fdata[1]
        rstr = explain_rstr(fdef)
        opt = fdef['option'] if 'option' in fdef else None
        fields.append(k)
        types.append(fdef['type'])
        descs.append(fdef['desc'])
        opts.append(opt)
        rstrs.append(rstr)

    # 사용할 헤더만 검사
    if sum([1 for o in opts if o is not None]) > 0:
        headers.append('Optional')
    if sum([1 for r in rstrs if r != '']) > 0:
        headers.append('Restrict')

    rows = []
    for i, f in enumerate(fields):
        row = [f, types[i], descs[i]]
        if 'Optional' in headers:
            row.append(opts[i])
        if 'Restrict' in headers:
            row.append(rstrs[i])
        rows.append(row)
    tbl = tabulate(rows, headers=headers, tablefmt='psql')
    out.write(tbl)
    out.write('\n')


def _write_event(name, data, out, namef):
    dmp = _get_dmp(data[0])
    edef = data[1]
    qname = f'{dmp}{name}'
    if namef is not None and namef.search(qname) is None:
        return

    out.write('\n')
    out.write(f"Event : {qname}\n")
    out.write(f"Description : {edef['desc']}\n")
    _write_table(edef, out)


def text_from_labfile(data, cus_type, namef, out=None):
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
        _write_event(ename, edata, out, namef)

    return out.getvalue()


def _html_types(dom):

    def _html_type_table(tdef):
        out = StringIO()
        headers = ['BaseType', 'Description']
        row = [tdef['type'], tdef['desc']]
        rstr = explain_rstr(tdef)
        if rstr != '':
            headers.append('Restrict')
            row.append(rstr)

        out.write('<table>')
        out.write("<tr>")
        for header in headers:
            out.write(f'<th>{header}</th>')
        out.write("</tr>")
        out.write("<tr>")
        for col in row:
            out.write(f'<td>{col}</td>')
        out.write("</tr>")
        out.write('</table>')
        return out.getvalue()

    types = []
    for tname, tlst in dom['types'].items():
        td = tlst[-1]
        dmp = _get_dmp(td[0])
        tdef = td[1]
        qtname = f'{dmp}types.{tname}'
        table = _html_type_table(tdef)
        types.append([qtname, tdef['desc'], table])
    return types


def _html_events(dom):

    def _html_event_table(edef):
        out = StringIO()

        headers = ['Field', 'Type', 'Description']
        fields = []
        types = []
        descs = []
        opts = []
        rstrs = []
        for k, v in edef['fields'].items():
            fdata = v[-1]
            fdef = fdata[1]
            rstr = explain_rstr(fdef, '<br>')
            opt = fdef['option'] if 'option' in fdef else None
            fields.append(k)
            types.append(fdef['type'])
            descs.append(fdef['desc'])
            opts.append(opt)
            rstrs.append(rstr)

        # 사용할 헤더만 검사
        if sum([1 for o in opts if o is not None]) > 0:
            headers.append('Optional')
        if sum([1 for r in rstrs if r != '']) > 0:
            headers.append('Restrict')

        out.write('<table>\n')
        out.write('<tr>\n')
        for h in headers:
            out.write(f'<th>{h}</th>\n')
        out.write('</tr>\n')

        for i, f in enumerate(fields):
            out.write('<tr>\n')
            out.write(f'<td>{f}</td>\n')
            out.write(f'<td>{types[i]}</td>\n')
            out.write(f'<td>{descs[i]}</td>\n')
            if 'Optional' in headers:
                out.write(f'<td>{opt}</td>\n')
            if 'Restrict' in headers:
                out.write(f'<td>{rstrs[i]}</td>\n')
            out.write('</tr>\n')
        out.write('</table>\n')
        return out.getvalue()

    events = []
    for name, data in dom.events.items():
        edata = data[-1]
        dmp = _get_dmp(edata[0])
        edef = edata[1]
        qname = f'{dmp}{name}'
        table = _html_event_table(edef)
        events.append([qname, edef['desc'], table])
    return events


def html_from_labfile(data, kwargs, cus_type):
    """랩 파일에서 HTML 파일 생성.

    Args:
        data (dict): 랩 파일 데이터
        kwargs (dict): 템플릿 렌더링시 사용하는 인자
        cus_type (bool): 커스텀 타입 출력 여부. 기본 False

    Returns:
        str: 결과 HTML
    """
    dom = build_dom(data, cus_type)
    assert type(kwargs) is dict
    home_dir = absdir_for_html(LOGLAB_HOME)
    kwargs['ext_dir'] = os.path.join(home_dir, 'extern')

    # custom types
    if 'types' in dom and cus_type:
        types = _html_types(dom)
        kwargs['types'] = types

    # events
    kwargs['events'] = _html_events(dom)

    tmpl_dir = os.path.join(LOGLAB_HOME, "template")
    loader = FileSystemLoader(tmpl_dir)
    env = Environment(loader=loader)
    tmpl = env.get_template("tmpl_doc.html.jinja")
    return tmpl.render(dom=dom, **kwargs)
