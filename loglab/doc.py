"""랩 파일에서 출력용 문서 생성."""

import os
import shutil
import textwrap
from io import StringIO

from jinja2 import Environment, FileSystemLoader
from tabulate import tabulate
from wcwidth import wcswidth

from loglab.model import build_model
from loglab.util import LOGLAB_HOME, absdir_for_html, explain_rstr, get_object_warn

SCR_WIDTH = shutil.get_terminal_size((80, 20)).columns
T_DESC_WIDTH = int(SCR_WIDTH * 0.35)
T_RSTR_WIDTH = int(SCR_WIDTH * 0.35)
E_DESC_WIDTH = int(SCR_WIDTH * 0.2)
E_RSTR_WIDTH = int(SCR_WIDTH * 0.2)


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
    return f"{domain}." if len(domain) > 0 else ""


def _write_type_table(tdef, out, keep_text, lang):

    headers = ["BaseType", "Description"]
    desc = tdef["desc"]
    w_desc = wcswidth(desc)
    if not keep_text and w_desc >= T_DESC_WIDTH:
        desc = textwrap.fill(desc, width=T_DESC_WIDTH)
    row = [tdef["type"], desc]
    rstr = explain_rstr(tdef, lang)
    w_rstr = wcswidth(rstr)

    if rstr != "":
        headers.append("Restrict")
        if not keep_text and w_rstr >= T_RSTR_WIDTH:
            rstr = textwrap.fill(rstr, width=T_RSTR_WIDTH)
        row.append(rstr)

    tbl = tabulate([row], headers, tablefmt="psql")
    out.write(tbl)
    out.write("\n")


def _write_custom_types(model, out, namef, keep_text, lang):
    # 출력할 것이 있는지 확인
    cnt = 0
    for tname, tlst in model["types"].items():
        td = tlst[-1]
        dmp = _get_dmp(td[0])
        qtname = f"{dmp}types.{tname}"
        if namef is None or namef.search(qtname) is not None:
            cnt += 1
    if cnt > 0:
        out.write("\n")

    for tname, tlst in model["types"].items():
        td = tlst[-1]
        dmp = _get_dmp(td[0])
        tdef = td[1]
        qtname = f"{dmp}types.{tname}"
        if namef is not None and namef.search(qtname) is None:
            continue

        out.write(f"Type : {qtname}\n")
        out.write(f"Description : {tdef['desc']}\n")
        _write_type_table(tdef, out, keep_text, lang)
        out.write("\n")


def _write_table(edef, out, keep_text, lang):
    headers = ["Field", "Type", "Description"]
    fields = []
    types = []
    descs = []
    opts = []
    rstrs = []

    for k, v in edef["fields"].items():
        fdata = v[-1]
        fdef = fdata[1]
        rstr = explain_rstr(fdef, lang)
        opt = fdef["option"] if "option" in fdef else None
        fields.append(k)
        types.append(fdef["type"])
        desc = fdef["desc"]
        w_desc = wcswidth(desc)
        w_rstr = wcswidth(rstr)
        if not keep_text and w_desc >= E_DESC_WIDTH:
            desc = textwrap.fill(desc, width=E_DESC_WIDTH)
        descs.append(desc)
        opts.append(opt)
        if not keep_text and w_rstr >= E_RSTR_WIDTH:
            rstr = textwrap.fill(rstr, width=E_RSTR_WIDTH)
        rstrs.append(rstr)

    # 사용할 헤더만 검사
    if sum([1 for o in opts if o is not None]) > 0:
        headers.append("Optional")
    if sum([1 for r in rstrs if r != ""]) > 0:
        headers.append("Restrict")

    rows = []
    for i, f in enumerate(fields):
        row = [f, types[i], descs[i]]
        if "Optional" in headers:
            row.append(opts[i])
        if "Restrict" in headers:
            row.append(rstrs[i])
        rows.append(row)
    tbl = tabulate(rows, headers=headers, tablefmt="psql")
    out.write(tbl)
    out.write("\n")


def _write_event(name, data, out, namef, keep_text, lang):
    dmp = _get_dmp(data[0])
    edef = data[1]
    qname = f"{dmp}{name}"
    if namef is not None and namef.search(qname) is None:
        return

    out.write("\n")
    opt = " (옵션)" if "option" in edef and edef["option"] else ""
    out.write(f"Event : {qname}{opt}\n")
    out.write(f"Description : {edef['desc']}\n")
    _write_table(edef, out, keep_text, lang)


def text_from_labfile(data, cus_type, namef, keep_text, lang, out=None):
    """랩 파일에서 텍스트 문서 생성.

    Args:
        data (dict): 랩 데이터
        cus_type (bool): 커스텀 타입 출력 여부. 기본 False
        namef (str): 이름 필터
        keep_text (bool): 긴 문자열 그대로 출력 여부
        lang (str): 언어 코드
        out (StringIO): 문자열 IO

    """
    if out is None:
        out = StringIO()

    model = build_model(data, lang, cus_type)
    # 도메인
    out.write("\n")
    out.write(f"Domain : {model.domain.name}\n")
    if "desc" in model.domain:
        out.write("Description : {}\n".format(model.domain.desc))
    if "version" in model.domain:
        out.write("Version : {}\n".format(model.domain.version))

    # 커스텀 타입
    if "types" in model and cus_type:
        _write_custom_types(model, out, namef, keep_text, lang)

    # 각 이벤트별로
    for ename, elst in model.events.items():
        edata = elst[-1]
        dname = edata[0]
        # 자기 도메인 것만 출력
        if dname != "":
            continue
        _write_event(ename, edata, out, namef, keep_text, lang)

    return out.getvalue()


def _html_types(model, lang):

    def _html_type_table(tdef):
        """단일 커스텀 타입을 HTML 테이블로 변환.

        Args:
            tdef (dict): 타입 정의

        Returns:
            str: HTML 테이블 문자열
        """
        out = StringIO()
        headers = ["BaseType", "Description"]
        row = [tdef["type"], tdef["desc"]]
        rstr = explain_rstr(tdef, lang)
        if rstr != "":
            headers.append("Restrict")
            row.append(rstr)

        out.write("<table>")
        out.write("<tr>")
        for header in headers:
            out.write(f"<th>{header}</th>")
        out.write("</tr>")
        out.write("<tr>")
        for i, col in enumerate(row):
            style = ""
            if i == 2:
                style = ' style="word-wrap: break-word; max-width: 30%"'
            out.write(f"<td{style}>{col}</td>")
        out.write("</tr>")
        out.write("</table>")
        return out.getvalue()

    types = []
    for tname, tlst in model["types"].items():
        td = tlst[-1]
        dmp = _get_dmp(td[0])
        tdef = td[1]
        qtname = f"{dmp}types.{tname}"
        table = _html_type_table(tdef)
        types.append([qtname, tdef["desc"], table])
    return types


def _html_events(model, lang):

    def _html_event_table(edef, lang):
        """단일 이벤트를 HTML 테이블로 변환.

        Args:
            edef (dict): 이벤트 정의
            lang (str): 언어 코드

        Returns:
            str: HTML 테이블 문자열
        """
        out = StringIO()

        headers = ["Field", "Type", "Description"]
        fields = []
        types = []
        descs = []
        opts = []
        rstrs = []
        for k, v in edef["fields"].items():
            fdata = v[-1]
            fdef = fdata[1]
            rstr = explain_rstr(fdef, lang, "<br>")
            opt = fdef["option"] if "option" in fdef else None
            fields.append(k)
            types.append(fdef["type"])
            descs.append(fdef["desc"])
            opts.append(opt)
            rstrs.append(rstr)

        # 사용할 헤더만 검사
        if sum([1 for o in opts if o is not None]) > 0:
            headers.append("Optional")
        if sum([1 for r in rstrs if r != ""]) > 0:
            headers.append("Restrict")

        out.write("<table>\n")
        out.write("<tr>\n")
        for header in headers:
            out.write(f"<th>{header}</th>\n")
        out.write("</tr>\n")

        for i, f in enumerate(fields):
            out.write("<tr>\n")
            out.write(f"<td>{f}</td>\n")
            out.write(f'<td style="text-align: center">{types[i]}</td>\n')
            out.write(f"<td>{descs[i]}</td>\n")
            if "Optional" in headers:
                opt = "옵션" if opts[i] else ""
                out.write(f'<td style="text-align: center">{opt}</td>\n')
            if "Restrict" in headers:
                style = ""
                if "Restrict" in header:
                    style = ' style="word-wrap: break-word; width: 25%"'
                out.write(f"<td{style}>{rstrs[i]}</td>\n")
            out.write("</tr>\n")
        out.write("</table>\n")
        return out.getvalue()

    events = []
    for name, data in model.events.items():
        edata = data[-1]
        dmp = _get_dmp(edata[0])
        edef = edata[1]
        opt = " (옵션)" if "option" in edef and edef["option"] else ""
        qname = f"{dmp}{name}{opt}"
        table = _html_event_table(edef, lang)
        events.append([qname, edef["desc"], table])
    return events


def html_from_labfile(data, kwargs, cus_type, lang):
    """랩 파일에서 HTML 파일 생성.

    Args:
        data (dict): 랩 파일 데이터
        kwargs (dict): 템플릿 렌더링시 사용하는 인자
        cus_type (bool): 커스텀 타입 출력 여부. 기본 False

    Returns:
        str: 결과 HTML
    """
    model = build_model(data, lang, cus_type)
    assert type(kwargs) is dict
    home_dir = absdir_for_html(LOGLAB_HOME)
    kwargs["ext_dir"] = os.path.join(home_dir, "extern")

    # custom types
    if "types" in model and cus_type:
        types = _html_types(model)
        kwargs["types"] = types

    # events
    kwargs["events"] = _html_events(model, lang)

    tmpl_dir = os.path.join(LOGLAB_HOME, "template")
    loader = FileSystemLoader(tmpl_dir)
    env = Environment(loader=loader)
    tmpl = env.get_template("tmpl_doc.html.jinja")
    return tmpl.render(model=model, **kwargs)


_type_json2cs = {
    "integer": "int",
    "number": "float",
    "string": "string",
    "boolean": "bool",
    "datetime": "DateTime",
}

_type_json2py = {
    "integer": "int",
    "number": "float",
    "string": "str",
    "boolean": "bool",
    "datetime": "datetime",
}

_type_json2cpp = {
    "integer": "int",
    "number": "float",
    "string": "std::string",
    "boolean": "bool",
    "datetime": "std::string",
}


def _type_cs(field):
    if "objtype" in field and "cs" in field["objtype"]:
        return field["objtype"]["cs"]
    else:
        return _type_json2cs[field["type"]]


def _type_py(field):
    if "objtype" in field and "py" in field["objtype"]:
        return field["objtype"]["py"]
    else:
        return _type_json2py[field["type"]]


def _type_cpp(field):
    if "objtype" in field and "cpp" in field["objtype"]:
        return field["objtype"]["cpp"]
    else:
        return _type_json2cpp[field["type"]]


def _object_required_filter(fields):
    rfields = dict()
    for fname in fields.keys():
        if fname == "DateTime":
            continue
        field = fields[fname][-1][1]
        if "option" in field and field["option"]:
            continue
        if "const" in field:
            continue
        rfields[fname] = fields[fname]
    return rfields


def _object_optional_filter(fields):
    ofields = dict()
    for fname in fields.keys():
        if fname == "DateTime":
            continue
        field = fields[fname][-1][1]
        if "option" not in field or not field["option"]:
            continue
        if "const" in field:
            continue
        ofields[fname] = fields[fname]
    return ofields


def _object_const_filter(fields):
    cfields = dict()
    for fname in fields.keys():
        field = fields[fname][-1][1]
        if "const" not in field:
            continue
        ctype = field["type"]
        cval = fields[fname][0][1]["const"]
        if type(cval) is list:
            cval = cval[0]
        cfields[fname] = (ctype, cval)
    return cfields


def object_from_labfile(data, code_type, lang):
    """

    로그 쓰기용 객체 출력.

    Args:
        data (dict): 랩 파일 데이터
        lang (str): 언어 코드
        output (str): 저장할 코드 파일 경로

    """
    assert code_type in ("cs", "py", "cpp")
    model = build_model(data, lang)
    tmpl_dir = os.path.join(LOGLAB_HOME, "template")
    loader = FileSystemLoader(tmpl_dir)
    env = Environment(loader=loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.filters["required"] = _object_required_filter
    env.filters["optional"] = _object_optional_filter
    env.filters["const"] = _object_const_filter
    tmpl = env.get_template(f"tmpl_obj.{code_type}.jinja")
    if code_type == "cs":
        _type = _type_cs
    elif code_type == "py":
        _type = _type_py
    else:
        _type = _type_cpp
    domain = data["domain"]
    events = model["events"]
    warn = get_object_warn(lang)
    kwargs = dict(domain=domain, events=events, warn=warn)
    return tmpl.render(type=_type, **kwargs)
