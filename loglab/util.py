"""유틸리티 모음."""
import os
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlparse
import json

from jsonschema import validate

LOGLAB_HOME = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()


def verify_labfile(lab_path, scm_path=None):
    """랩파일을 검증.

    Args:
        lab_path (str): 랩파일 URI
        scm_path (str): 스키마 파일 URI

    """
    if scm_path is None:
        scm_path = os.path.join(LOGLAB_HOME, 'schema/lab.schema.json')
    schema = load_file_from(scm_path)
    schema = json.loads(schema)
    lab = load_file_from(lab_path)
    lab = json.loads(lab)

    validate(lab, schema=schema)


def load_file_from(path):
    """지정된 로컬 또는 웹에서 텍스트 파일 읽기.

    Args:
        path (str): 로컬 파일 경로 또는 URI

    Returns:
        str: 읽어들인 파일 내용
    """
    parsed = urlparse(path)
    if parsed.scheme in ('http', 'https'):
        # 웹 파일
        with urlopen(path) as f:
            return f.read()
    else:
        # 로컬 파일
        with open(path, 'rt') as f:
            return f.read()