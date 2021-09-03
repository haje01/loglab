"""유틸리티 모음."""
import os
from pathlib import Path
import json

from jsonschema import validate

LOGLAB_HOME = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()


def verify_labfile(labfile):
    sfile = os.path.join(LOGLAB_HOME, "schema/lab.schema.json")
    with open(sfile, 'rt') as f:
        schema = f.read()
        schema = json.loads(schema)

    with open(labfile, 'rt') as f:
        body = f.read()
        body = json.loads(body)

    validate(body, schema=schema)


if __name__ == '__main__':
    # 테스트용
    verify_labfile(os.path.join(LOGLAB_HOME, "schema/test.lab.json"))