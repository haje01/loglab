"""랩 파일에서 로그용 JSON 스키마 생성."""
import os
import sys
import copy
import json
from collections import defaultdict

from jsonschema import validate, ValidationError
from jinja2 import Environment, FileSystemLoader
from requests.api import request

from loglab.dom import build_dom
from loglab.util import AttrDict, load_file_from, LOGLAB_HOME


def verify_labfile(lab_path, scm_path=None, err_exit=True):
    """랩 파일을 검증.

    Args:
        lab_path (str): 랩 파일 URI
        scm_path (str): 스키마 파일 URI
        err_exit (bool): 에러 발생시 종료 여부. 기본 True

    Returns:
        str: 읽어들인 랩 파일 JSON 을 재활용할 수 있게 반환

    """
    if scm_path is None:
        scm_path = os.path.join(LOGLAB_HOME,
                                'schema', 'lab.schema.json')

    try:
        schema = load_file_from(scm_path)
        schema = json.loads(schema)
        body = load_file_from(lab_path)
        lab = json.loads(body)
        validate(lab, schema=schema)
    except Exception as e:
        print("Error: 랩 파일 검증 에러")
        print(str(e))
        if err_exit:
            sys.exit(1)
    else:
        return lab


def log_schema_from_labfile(data):
    """랩 데이터에서 로그용 JSON 스키마 생성.

    Args:
        data (dict): 랩 데이터

    """
    def _resolve_type(typ, v, domain):
        elms = typ.split('.')
        assert len(elms) == 2, f"잘못된 형식의 타입입니다: {typ}"
        tname = elms[1]
        types = data['types'] if domain == '' else data['_imported_'][domain]['types']
        assert tname in types.keys(), \
            f"정의되지 않은 타입입니다: {typ}"
        tdef = types[tname]
        if len(v) == 2:
            v.append(None)
        v = [tdef['type'], v[1], v[2], None, tdef]
        return v

    dom = build_dom(data)
    events = []
    items = []
    for ename, elst in dom.events.items():
        edata = AttrDict(elst[-1][1])
        item = f'{{"$ref": "#/$defs/{ename}"}}'
        items.append(item)
        fields = edata.fields
        reqs = []
        props = [f'"Event": {{"const": "{ename}"}}']
        for k, v in fields.items():
            v = v[-1]
            elms = k.split('.')
            # fdm = '.'.join(elms[:-1])
            fnm = elms[-1]
            typ = v[1]['type']
            desc = v[1]['desc']
            if typ == "datetime":
                prop = f"""
                "{fnm}": {{
                    "type": "string",
                    "description": "{desc}",
                    "pattern": "^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)(\\\\.[0-9]+)?(([Zz])|([\\\\+|\\\\-]([01][0-9]|2[0-3]):[0-5][0-9]))$"
                }}"""
            else:
                # if 'types' in typ:
                #     v = _resolve_type(typ, v, fdm)
                finfo = {
                    "type": typ,
                    "description": desc
                }
                for rk, rv in v[1].items():
                    if rk in ('type', 'desc'):
                        continue
                    if rk == 'enum' and len(rv) > 0 and type(rv[0]) is list:
                        rv = [r[0] for r in rv]
                    finfo[rk] = rv
                body = json.dumps(finfo, ensure_ascii=False)
                prop = f"""
                "{fnm}": {body}"""
            if 'option' not in v[1] or v[1]['option'] == False:
                rf = f'"{fnm}"'
                if rf not in reqs:
                    reqs.append(f'"{fnm}"')
            props.append(prop)
        props = ",".join(props)
        reqs = ", ".join(reqs)
        # fields = f"""
        # """
        ebody = f"""
            "type": "object",
            "properties": {{
                {props}
            }},
            "required": [{reqs}],
            "additionalProperties": false
        """
        events.append(f'"{ename}" : {{\n      {ebody}')
    events = '\n        },\n        '.join(events)
    events += "}"
    items = ",\n            ".join(items)
    return f'''
{{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "{dom.domain.name}",
    "description": "{dom.domain.desc}",
    "type": "array",
    "$defs": {{
        {events}
    }},
    "items": {{
        "oneOf": [
            {items}
        ]
    }}
}}
    '''


def flow_schema_from_labfile(labfile, data):
    """랩 데이터 에서 플로우 JSON 스키마 생성.

    Args:
        labfile (str): 랩 파일 경로
        data (dict): 랩 데이터

    """
    def _collect(fields, group):
        for k, v in group.items():
            if 'fields' in v:
                for field in v['fields']:
                    if type(field) is dict:
                        fields.add(field['name'])
                    else:
                        fields.add(field[0])

    def _collect_all_fields(data):
        fields = set()
        if 'bases' in data:
            _collect(fields, data['bases'])
        if 'events' in data:
            _collect(fields, data['events'])
        return fields

    events = list(data['events'].keys())
    fields = _collect_all_fields(data)
    tmpl_path = os.path.join(LOGLAB_HOME, "template")
    loader = FileSystemLoader(tmpl_path)
    env = Environment(loader=loader)
    tmpl = env.get_template("tmpl_flow.json")
    return tmpl.render(labfile=labfile, events=events, fields=fields)


def verify_logfile(schema, logfile):
    """로그 파일을 스키마로 검증.

    Args:
        schema (str): 로그 스키마 파일 경로
        logfile (str): 검증할 로그 파일 경로

    """
    # 로그 스키마에서 이벤트별 스키마 생성
    evt_scm = {}
    with open(schema, 'rt', encoding='utf8') as f:
        body = f.read()
        try:
            scmdata = json.loads(body)
        except json.decoder.JSONDecodeError as e:
            print("Error: 로그랩이 생성한 JSON 스키마 에러. 로그랩 개발자에 문의 요망.")
            print(e)
            sys.exit(1)

        for ref in scmdata['items']['oneOf']:
            scm = copy.deepcopy(scmdata)
            evt = ref['$ref'].split('/')[-1]
            # 다른 이벤트는 제거
            defs = {}
            defs[evt]=scm['$defs'][evt]
            scm['$defs'] = defs
            scm['items'] = ref
            evt_scm[evt] = scm

    # 이벤트별 로그 모음
    evt_lnos = defaultdict(list)
    evt_logs = defaultdict(list)
    with open(logfile, 'rt', encoding='utf8') as f:
        for lno, line in enumerate(f):
            try:
                log = json.loads(line)
            except json.decoder.JSONDecodeError as e:
                print(f"Error: [Line: {lno + 1}] 유효한 JSON 형식이 아닙니다.")
                print(e)
                sys.exit(1)

            if 'Event' not in log or log['Event'] not in evt_scm:
                import pdb; pdb.set_trace()
                print("Error: 스키마에서 이벤트를 찾을 수 없습니다")
                print(f"Line {lno}: {line}")
                sys.exit(1)

            evt = log['Event']
            evt_lnos[evt].append(lno)
            data = json.loads(line)
            evt_logs[evt].append(data)

    # 이벤트별로 검증
    for evt, elogs in evt_logs.items():
        escm = evt_scm[evt]
        elogs = evt_logs[evt]
        try:
            validate(elogs, schema=escm)
        except ValidationError as e:
            no = list(e.absolute_path)[0]
            lno = evt_lnos[evt][no]
            log = evt_logs[evt][no]
            print(f"Error: [Line: {lno + 1}] {e.message}")
            print(log)
            sys.exit(1)