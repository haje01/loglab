"""랩 파일에서 로그용 JSON 스키마 생성."""
import os
import sys
import copy
import json
from collections import defaultdict

from jsonschema import validate, ValidationError
from jinja2 import Environment, FileSystemLoader
from requests.api import request

from loglab.model import build_model
from loglab.util import AttrDict, load_file_from, LOGLAB_HOME


def recursive_validate(lab, schema, lab_path):
    """lab 파일과 그것이 import하는 모든 파일들을 재귀적으로 검증.
    
    Args:
        lab (dict): 검증할 lab 파일 데이터
        schema (dict): 검증에 사용할 JSON 스키마
        lab_path (str): lab 파일의 경로 (에러 메시지용)
        
    Raises:
        Exception: 검증 실패시 상세 에러 메시지와 함께
    """
    # 참조하는 lab 이 있으면 그것도 검증
    if 'import' in lab:
        basedir = os.path.dirname(lab_path)
        for imp in lab['import']:
            try:
                ipath = os.path.join(basedir, f'{imp}.lab.json')
                ibody = load_file_from(ipath)
                ilab = json.loads(ibody)
                recursive_validate(ilab, schema, ipath)
            except Exception as e:
                raise Exception(str(e) + f"\nValidation Error at {ipath}")
    validate(lab, schema)


def verify_labfile(lab_path, scm_path=None, err_exit=True):
    """lab 파일의 구조와 내용을 JSON 스키마로 검증.
    
    lab 파일이 올바른 구조를 가지고 있는지, 필수 필드들이 있는지,
    타입과 제약 조건이 맞는지 등을 종합적으로 검증함.
    import하는 파일들도 재귀적으로 검증.

    Args:
        lab_path (str): 검증할 랩 파일 경로
        scm_path (str, optional): 사용할 스키마 파일 경로. None이면 기본 스키마 사용
        err_exit (bool): 에러 발생시 프로그램 종료 여부. 기본 True

    Returns:
        dict: 검증이 완료된 랩 파일 데이터 (성공시에만)
        
    Raises:
        SystemExit: err_exit=True이고 검증 실패시
    """
    if scm_path is None:
        scm_path = os.path.join(LOGLAB_HOME,
                                'schema', 'lab.schema.json')

    try:
        schema = load_file_from(scm_path)
        schema = json.loads(schema)
        body = load_file_from(lab_path)
        lab = json.loads(body)
        recursive_validate(lab, schema, lab_path)
    except Exception as e:
        print("Error: 랩 파일 검증 에러")
        print(str(e))
        if 'Validation Error at' not in str(e):
            print(f"Validation Error at {lab_path}")
        if err_exit:
            sys.exit(1)
    else:
        return lab


def log_schema_from_labfile(data):
    """lab 파일 데이터로부터 실제 로그 검증용 JSON 스키마를 동적 생성.
    
    lab 파일에 정의된 이벤트들을 분석하여 각 이벤트별로 JSON 스키마를 생성하고,
    이를 통합한 최종 로그 검증 스키마를 만듦. 생성된 스키마는 JSON Lines 형태의
    로그 파일을 검증하는데 사용됨.

    Args:
        data (dict): 빌드된 lab 모델 데이터
        
    Returns:
        str: JSON 형태의 로그 검증 스키마 문자열
    """
    def _resolve_type(typ, v, domain):
        """커스텀 타입을 실제 타입 정의로 해결.
        
        Args:
            typ (str): 타입 이름 ('types.typename' 형태)
            v (list): 필드 값 정보
            domain (str): 도메인 경로
            
        Returns:
            list: 해결된 타입 정보가 포함된 필드 값
            
        Raises:
            AssertionError: 타입 형식이 잘못되었거나 정의되지 않은 타입인 경우
        """
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

    dom = build_model(data)
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
                    "pattern": "^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)(\\\\.[0-9]+)?(([Zz])|([\\\\+|\\\\-]([01][0-9]|2[0-3]):?[0-5][0-9]))$"
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
                    if rk == 'enum' and len(rv) > 0:
                        ev = []
                        for r in rv:
                            if type(r) is list:
                                ev.append(r[0])
                            else:
                                ev.append(r)
                        rv = ev
                    elif rk == 'const' and len(rv) > 0:
                        if type(rv) is list:
                            rv = rv[0]
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


def verify_logfile(schema, logfile):
    """실제 로그 파일이 생성된 스키마에 맞는지 검증.
    
    JSON Lines 형태의 로그 파일을 한 줄씩 읽어서 각 로그 엔트리가
    해당 이벤트의 스키마에 맞는지 검증함. 오류 발생시 정확한 라인 번호와
    오류 내용을 제공.

    Args:
        schema (str): 로그 검증용 JSON 스키마 파일 경로
        logfile (str): 검증할 로그 파일 경로
        
    Raises:
        SystemExit: 스키마 파일이 잘못되었거나 로그 검증 실패시
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
