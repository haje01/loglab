"""랩파일에서 로그용 JSON 스키마 생성."""
import os
import json

from jsonschema import validate
from jinja2 import Environment, BaseLoader

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


def json_schema_from_labfile(labjs):
    """랩파일 데이터에서 JSON 스키마 생성.

    Args:
        labjs (dict): 랩파일 내용

    """
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
            if v[0] == "datetime":
                prop = f"""
                "{k}": {{
                    "type": "string",
                    "description": "{v[1]}",
                    "format": "date-time"
                }}"""
            else:
                prop = f"""
                "{k}": {{
                    "type": "{v[0]}",
                    "description": "{v[1]}"
                }}"""
            if len(v) <= 2 or v[2] == False:
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