"""랩파일에서 로그용 JSON 스키마 생성."""
import os
import sys
import copy
import json
from collections import defaultdict

from jinja2.loaders import PackageLoader

from jsonschema import validate, ValidationError
from jinja2 import Environment, FileSystemLoader

from loglab.util import AttrDict, load_file_from, LOGLAB_HOME,\
    fields_from_entity


def verify_labfile(lab_path, scm_path=None):
    """랩파일을 검증.

    Args:
        lab_path (str): 랩파일 URI
        scm_path (str): 스키마 파일 URI

    Returns:
        str: 읽어들인 랩파일 JSON 을 재활용할 수 있게 반환

    """
    if scm_path is None:
        scm_path = os.path.join(LOGLAB_HOME,
            'schema/lab.schema.json')
    schema = load_file_from(scm_path)
    schema = json.loads(schema)
    body = load_file_from(lab_path)
    labjs = json.loads(body)

    validate(labjs, schema=schema)
    return labjs


def log_schema_from_labfile(labjs):
    """랩파일 데이터에서 로그용 JSON 스키마 생성.

    Args:
        labjs (dict): 랩파일 데이터

    """
    def _resolve_type(typ, v):
        elms = typ.split('.')
        assert len(elms) == 2, f"잘못된 형식의 타입입니다: {typ}"
        tname = elms[1]
        assert tname in labjs['types'].keys(), \
            f"정의되지 않은 타입입니다: {typ}"
        tdef = labjs['types'][tname]
        if len(v) == 2:
            v.append(None)
        v = [tdef['type'], v[1], v[2], None, tdef]
        return v

    lab = AttrDict(labjs)
    events = []
    items = []
    for ename, ebody in lab.events.items():
        item = f'{{"$ref": "#/$defs/{ename}"}}'
        items.append(item)
        fields = fields_from_entity(lab, ebody)
        reqs = []
        props = [f'"Event": {{"const": "{ename}"}}']
        for k, v in fields.items():
            typ = v[0]
            if typ == "datetime":
                prop = f"""
                "{k}": {{
                    "type": "string",
                    "description": "{v[1]}",
                    "format": "date-time"
                }}"""
            else:
                if 'types' in typ:
                    v = _resolve_type(typ, v)
                finfo = {
                    "type": typ,
                    "description": v[1]
                }
                if len(v) == 5:
                    for rk, rv in v[4].items():
                        finfo[rk] = rv
                body = json.dumps(finfo, ensure_ascii=False)
                prop = f"""
                "{k}": {body}"""
            if len(v) <= 2 or v[2] in (False, None):
                reqs.append(f'"{k}"')
            props.append(prop)
        props = ",".join(props)
        reqs = ", ".join(reqs)
        fields = f"""
        """
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
    "title": "{lab.domain.name}",
    "description": "{lab.domain.desc}",
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


def flow_schema_from_labfile(labfile, labjs):
    """랩파일 데이터에서 플로우 JSON 스키마 생성.

    Args:
        labfile (str): 랩파일 경로
        labjs (dict): 랩파일 데이터

    """
    def _collect(fields, group):
        for k, v in group.items():
            if 'fields' in v:
                for field in v['fields']:
                    if type(field) is dict:
                        fields.add(field['name'])
                    else:
                        fields.add(field[0])

    def _collect_all_fields(labjs):
        fields = set()
        if 'bases' in labjs:
            _collect(fields, labjs['bases'])
        if 'events' in labjs:
            _collect(fields, labjs['events'])
        return fields

    events = list(labjs['events'].keys())
    fields = _collect_all_fields(labjs)
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
    with open(schema, 'rt') as f:
        body = f.read()
        scmdata = json.loads(body)
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
    with open(logfile, 'rt') as f:
        for lno, line in enumerate(f):
            log = json.loads(line)
            if 'Event' not in log or log['Event'] not in evt_scm:
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