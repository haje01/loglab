"""유틸리티 모음."""
import os
import sys
import copy
from glob import glob
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlparse
from collections import OrderedDict
from pathlib import Path
from glob import glob
from shutil import rmtree

from requests import get


LOGLAB_HOME = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
RESULT_DIR = '.loglab'
TEMP_DIR = os.path.join(RESULT_DIR, 'temp')
IMPORT_DIR = os.path.join(RESULT_DIR, 'import')
BUILTIN_TYPES = ('string', 'integer', 'number', 'boolean', 'datetime')

class AttrDict(dict):
    """dict 키를 속성처럼 접근하는 헬퍼."""
    def __init__(self, *args, **kwargs):
        def from_nested_dict(data):
            """ Construct nested AttrDicts from nested dictionaries. """
            if not isinstance(data, dict):
                return data
            else:
                return AttrDict({key: from_nested_dict(data[key])
                                    for key in data})

        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

        for key in self.keys():
            self[key] = from_nested_dict(self[key])


def find_labfile(labfile, print_msg=True):
    """사용할 랩 파일 디렉토리에서 찾기.

    - 지정된 랩 파일이 있으면 그것을,
    - 아니면 현재 디렉토리에서 유일한 랩 파일이 있으면 그것을
    - 현재 디렉토리에 랩 파일이 없거나 여럿 있으면 Error

    Args:
        labfile (str): 랩 파일 경로
        print_msg (bool): 메시지 출력 여부. 기본 True

    Returns:
        str: 찾은 랩 파일의 절대 경로

    """
    def handle(labfile, print_msg):
        labfile = os.path.abspath(labfile)
        if print_msg:
            print(f"[랩 파일 : {labfile}]")
        return labfile

    if labfile is not None:
        return handle(labfile, print_msg)

    labs = glob("*.lab.json")
    num_labs = len(labs)
    if num_labs == 1:
        return handle(labs[0], print_msg)
    elif num_labs == 0:
        print("Error: 현재 디렉토리에 랩 파일이 없습니다. 새 랩 파일을 "
              "만들거나, 사용할 랩 파일을 명시적으로 지정해 주세요.")
    else:
        print("Error: 현재 디렉토리에 랩 파일이 하나 이상 있습니다. "
              "사용할 랩 파일을 명시적으로 지정해 주세요.")
    sys.exit(1)


def find_log_schema(labfile, labjs, _schema):
    """로그 스키마 찾기.

    - 지정된 스키마가 있으면 그것을,
    - 아니면 현재 디렉토리에서 랩 파일의 도메인 이름에 준하는 로그 스키마가 있으면 그것을,
    - 아니면 Error

    Args:
        labfile (str): 랩 파일 경로
        labjs (dict): 랩 파일 데이터
        _schema (str): 지정된 스키마

    Return:
        str: 찾은 로그 스키마의 절대 경로

    """
    if _schema is not None:
        return os.path.abspath(_schema)

    # 랩 파일 도메인 이름에서 로그 스키마 파일명 유추
    if 'domain' in labjs or 'name' in labjs['domain']:
        domain = labjs['domain']['name']
        tmp_dir = request_tmp_dir(labfile)
        schema = os.path.join(tmp_dir, f'{domain}.log.schema.json')
        if os.path.isfile(schema):
            return schema


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


def _init_fields():
    fields = OrderedDict()
    fields["DateTime"] = ["datetime", "이벤트 일시"]
    return fields


def explain_rstr(f):
    """제약을 설명으로 변환."""
    exps = []
    atype = f['type']
    if atype in ('integer', 'number'):
        amin = amax = xmin = xmax = enum = None
        if 'minimum' in f:
            amin = f['minimum']
        if 'maximum' in f:
            amax = f['maximum']
        if 'exclusiveMinimum' in f:
            xmin = f['exclusiveMinimum']
        if 'exclusiveMaximum' in f:
            xmax = f['exclusiveMaximum']
        if 'enum' in f:
            enum = f['enum']
            if len(enum) > 0 and type(enum[0]) is list:
                expl = []
                for d in enum:
                    expl.append(f"{d[0]}: {d[1]}")
                enum = '\n'.join(expl)
            else:
                enum = f'{enum} 중 하나'

        assert amin is None or xmin is None,\
            'minimum 과 exclusiveMinimum 함께 사용 불가'
        assert amax is None or xmax is None,\
            'maximum 과 exclusiveMaximum 함께 사용 불가'

        stmts = []
        if amin is not None:
            stmts.append(f"{amin} 이상")
        if xmin is not None:
            stmts.append(f"{xmin} 초과")
        if amax is not None:
            stmts.append(f"{amax} 이하")
        if xmax is not None:
            stmts.append(f"{xmax} 미만")
        if enum is not None:
            exps.append(enum)

        if len(stmts) > 0:
            exps.append(' '.join(stmts))
    elif atype == 'string':
        minl = maxl = enum = ptrn = fmt = None
        if 'minLength' in f:
            minl = f['minLength']
        if 'maxLength' in f:
            maxl = f['maxLength']
        if 'enum' in f:
            enum = f['enum']
        if 'pattern' in f:
            ptrn = f['pattern']
        if 'format' in f:
            fmt = f['format']

        stmts = []
        if minl is not None:
            stmts.append(f"{minl} 자 이상")
        if maxl is not None:
            stmts.append(f"{maxl} 자 이하")
        if len(stmts) > 0:
            exps.append(' '.join(stmts))

        if enum is not None:
            exps.append(f"{enum} 중 하나")
        if ptrn is not None:
            exps.append(f"정규식 {ptrn} 매칭")
        if fmt is not None:
            exps.append(f"{fmt} 형식")
    return '\n'.join(exps)


# def fields_from_entity(root, entity, dmp, field_cb=None):
#     """랩 파일의 엔터티에서 필드 정보 얻기.

#     Args:
#         root (dict): 랩 파일 데이터
#         entity (dict): 엔터티 데이터
#         dmp (str): 도메인 접두어
#         field_cb (function): 필드값 변환 함수

#     """
#     def _parse_field(f):
#         """사전형 필드 정보 파싱."""
#         opt = f['option'] if 'option' in f else None
#         exrstr = explain_rstr(f)
#         name = f['name']
#         atype = f['type']
#         desc = f['desc']
#         # 제약만 남기기
#         rstr = copy.deepcopy(f)
#         del rstr['name']
#         del rstr['type']
#         del rstr['desc']
#         return [name, atype, desc, opt, exrstr, rstr]

#     fields = _init_fields()
#     # mixin 이 있으면 그것의 필드를 가져옴
#     if 'mixins' in entity:
#         _fields = _fields_from_mixins(root, entity['mixins'], domain)
#         fields.update(_fields)

#     # 엔터티 자체 필드 반영
#     if 'fields' in entity:
#         for f in entity['fields']:
#             # 사전형 필드 정보 파싱
#             if type(f) is dict:
#                 f = _parse_field(f)
#             fname = f'{domain}.{f[0]}' if domain is not None else f[0]
#             if field_cb is not None:
#                 fields[fname] = field_cb(f[1:])
#             else:
#                 fields[fname] = f[1:]
#     return fields


def request_tmp_dir(labfile=None):
    """랩 파일이 있는 경로에서 임시 파일용 디렉토리를 확보.

    랩 파일 경로가 없으면 현제 디렉토리를 이용

    Args:
        labfile (string): 랩 파일 경로

    """
    return _request_dir(labfile, TEMP_DIR)


def request_imp_dir(labfile=None):
    """랩 파일이 있는 경로에서 가져오기 파일용 디렉토리를 확보.

    랩 파일 경로가 없으면 현제 디렉토리를 이용

    Args:
        labfile (string): 랩 파일 경로

    """
    return _request_dir(labfile, IMPORT_DIR)


def _request_dir(labfile, subdir):
    if labfile is not None:
        adir = os.path.dirname(labfile)
    else:
        adir = os.getcwd()
    adir = os.path.join(adir, subdir)
    Path(adir).mkdir(parents=True, exist_ok=True)
    return adir


def download(url, filepath=None):
    """파일 다운로드.

    URL 에서 지정된 파일 경로로 파일 다운로드.
    지정된 파일 경로가 없으면 현재 디렉토리에서 URL 경로의 마지막 요소로 저장

    Args:
        url (string): 다운 받을 URL
        filepath (string): 저장할 파일 경로. 기본 None

    """
    if filepath is None:
        filepath = url.split('/')[-1]

    with open(filepath, "wb") as f:
        res = get(url)
        f.write(res.content)


def test_reset():
    """테스트 관련 초기화."""
    cwd = os.path.join(LOGLAB_HOME, 'tests')
    os.chdir(cwd)

    # 기존 파일 삭제
    for f in glob("*.lab.json"):
        os.remove(f)
    for f in glob("*.txt"):
        os.remove(f)
    if os.path.isdir(RESULT_DIR):
        # 결과 디렉토리 삭제
        rmtree(RESULT_DIR)
