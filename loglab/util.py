"""유틸리티 모음."""

import gettext
import os
import re
import sys
from glob import glob
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

from requests import get

# Python 3.9+ 에서는 importlib.resources, 이전 버전에서는 importlib_resources 사용
try:
    from importlib.resources import as_file, files
except ImportError:
    try:
        from importlib_resources import as_file, files
    except ImportError:
        # fallback: 기존 방식 사용
        files = None
        as_file = None

LOGLAB_HOME = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
BUILTIN_TYPES = ("string", "integer", "number", "boolean", "datetime")

lc_dir = os.path.join(LOGLAB_HOME, "locales")


def get_schema_file_content():
    """패키지에서 lab.schema.json 파일의 내용을 반환.

    패키지로 설치된 경우 importlib.resources를 사용하고,
    개발 환경에서는 기존 방식을 사용.

    Returns:
        str: schema 파일의 내용
    """
    if files is not None:
        try:
            # 패키지 리소스로 접근 시도
            import loglab

            schema_file = files(loglab) / "schema" / "lab.schema.json"
            if schema_file.is_file():
                return schema_file.read_text(encoding="utf-8")
        except Exception:
            pass

    # fallback: 기존 방식 사용
    schema_path = os.path.join(LOGLAB_HOME, "loglab", "schema", "lab.schema.json")
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Schema file not found: {schema_path}")


def get_schema_file_path():
    """패키지에서 lab.schema.json 파일의 경로를 반환.

    개발 환경에서는 실제 경로를 반환하고,
    패키지 설치된 경우에는 내용을 직접 읽도록 안내.

    Returns:
        str: schema 파일의 절대 경로 (fallback 용도)
    """
    return os.path.join(LOGLAB_HOME, "loglab", "schema", "lab.schema.json")


def get_translator(lang):
    """언어별 번역 함수를 반환.

    Args:
        lang (str): 언어 코드 (예: 'ko', 'en'). None이면 번역하지 않음

    Returns:
        callable: 번역 함수
    """
    if lang is None:
        return lambda x: x
    trans = gettext.translation("base", localedir=lc_dir, languages=(lang,))
    return trans.gettext


def get_dt_desc(lang):
    """DateTime 필드의 설명을 언어별로 반환.

    Args:
        lang (str): 언어 코드

    Returns:
        str: 번역된 DateTime 필드 설명
    """
    _ = get_translator(lang)
    return _("이벤트 일시")


def get_object_warn(lang):
    """생성된 코드 파일의 경고 메시지를 언어별로 반환.

    Args:
        lang (str): 언어 코드

    Returns:
        str: 번역된 경고 메시지
    """
    _ = get_translator(lang)
    return _("이 파일은 LogLab 에서 생성된 것입니다. 고치지 마세요!")


class AttrDict(dict):
    """dict 키를 속성처럼 접근하는 헬퍼 클래스.

    딕셔너리의 키를 obj.key 형태로 접근할 수 있게 해주며,
    중첩된 딕셔너리도 재귀적으로 AttrDict로 변환함.
    """

    def __init__(self, *args, **kwargs):
        def from_nested_dict(data):
            """중첩된 딕셔너리를 AttrDict로 재귀적으로 변환.

            Args:
                data: 변환할 데이터

            Returns:
                AttrDict 또는 원본 데이터
            """
            if not isinstance(data, dict):
                return data
            else:
                return AttrDict({key: from_nested_dict(data[key]) for key in data})

        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

        for key in self.keys():
            self[key] = from_nested_dict(self[key])


def find_labfile(labfile, print_msg=True):
    """사용할 랩 파일을 디렉토리에서 찾기.

    우선순위:
    1. 지정된 랩 파일이 있으면 그것을 사용
    2. 현재 디렉토리에서 유일한 랩 파일이 있으면 그것을 사용
    3. 현재 디렉토리에 랩 파일이 없거나 여럿 있으면 에러

    Args:
        labfile (str): 랩 파일 경로. None이면 자동 검색
        print_msg (bool): 메시지 출력 여부. 기본 True

    Returns:
        str: 찾은 랩 파일의 절대 경로

    Raises:
        SystemExit: 적절한 랩 파일을 찾을 수 없는 경우
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
        print(
            "Error: 현재 디렉토리에 랩 파일이 없습니다. 새 랩 파일을 "
            "만들거나, 사용할 랩 파일을 명시적으로 지정해 주세요."
        )
    else:
        print(
            "Error: 현재 디렉토리에 랩 파일이 하나 이상 있습니다. "
            "사용할 랩 파일을 명시적으로 지정해 주세요."
        )
    sys.exit(1)


def load_file_from(path):
    """로컬 파일 또는 웹 URL에서 텍스트 파일을 읽어옴.

    HTTP/HTTPS URL인 경우 웹에서 다운로드하고,
    그렇지 않으면 로컬 파일로 간주하여 읽음.

    Args:
        path (str): 로컬 파일 경로 또는 HTTP/HTTPS URL

    Returns:
        str: 읽어들인 파일 내용

    Raises:
        URLError: 웹 파일 다운로드 실패시
        FileNotFoundError: 로컬 파일이 존재하지 않는 경우
    """
    parsed = urlparse(path)
    if parsed.scheme in ("http", "https"):
        # 웹 파일
        with urlopen(path) as f:
            return f.read()
    else:
        # 로컬 파일
        with open(path, "rt", encoding="utf8") as f:
            return f.read()


# def _init_fields():
#     fields = {}
#     fields["DateTime"] = ["datetime", EDT_DESC]
#     return fields


def explain_rstr(f, lang, line_dlm="\n"):
    """필드의 제약 조건을 사람이 읽기 쉬운 설명으로 변환.

    JSON Schema의 제약 조건들(minimum, maximum, enum, pattern 등)을
    지정된 언어로 번역된 설명 문자열로 변환함.

    Args:
        f (dict): 필드 정의 딕셔너리 (type, 제약 조건들 포함)
        lang (str): 번역할 언어 코드
        line_dlm (str): 여러 제약 조건을 구분할 구분자. 기본 '\n'

    Returns:
        str: 번역된 제약 조건 설명 문자열
    """
    _ = get_translator(lang)
    exps = []
    atype = f["type"]
    if atype in ("integer", "number"):
        amin = amax = xmin = xmax = enum = const = None
        if "minimum" in f:
            amin = f["minimum"]
        if "maximum" in f:
            amax = f["maximum"]
        if "exclusiveMinimum" in f:
            xmin = f["exclusiveMinimum"]
        if "exclusiveMaximum" in f:
            xmax = f["exclusiveMaximum"]
        if "enum" in f:
            enum = f["enum"]
            if len(enum) > 0:
                expl = []
                for d in enum:
                    if type(d) is list:
                        expl.append(f"{d[0]} ({d[1]})")
                    else:
                        expl.append(str(d))
                enum = expl
            arr = ", ".join(expl)
            enum = _("{} 중 하나").format(arr)
        if "const" in f:
            const = f["const"]
            if type(const) is list:
                const = f"{const[0]} ({const[1]})"
            const = _("항상 {}").format(const)

        assert (
            amin is None or xmin is None
        ), "minimum 과 exclusiveMinimum 함께 사용 불가"
        assert (
            amax is None or xmax is None
        ), "maximum 과 exclusiveMaximum 함께 사용 불가"

        stmts = []
        if amin is not None:
            stmts.append(_("{} 이상").format(amin))
        if xmin is not None:
            stmts.append(_("{} 초과").format(xmin))
        if amax is not None:
            stmts.append(_("{} 이하").format(amax))
        if xmax is not None:
            stmts.append(_("{} 미만").format(xmax))
        if enum is not None:
            exps.append(enum)
        if const is not None:
            exps.append(const)

        if len(stmts) > 0:
            exps.append(" ".join(stmts))
    elif atype == "string":
        minl = maxl = enum = ptrn = fmt = None
        if "minLength" in f:
            minl = f["minLength"]
        if "maxLength" in f:
            maxl = f["maxLength"]
        if "enum" in f:
            enum = f["enum"]
        if "pattern" in f:
            ptrn = f["pattern"]
        if "format" in f:
            fmt = f["format"]

        stmts = []
        if minl is not None:
            stmts.append(_("{} 자 이상").format(minl))
        if maxl is not None:
            stmts.append(_("{} 자 이하").format(maxl))
        if len(stmts) > 0:
            exps.append(" ".join(stmts))

        if enum is not None:
            if type(enum[0]) is list:
                _enum = []
                for i, d in enum:
                    _enum.append(f"{i} ({d})")
                enum = _enum
            arr = ", ".join(str(e) for e in enum)
            exps.append(_("{} 중 하나").format(arr))
        if ptrn is not None:
            exps.append(_("정규식 {} 매칭").format(ptrn))
        if fmt is not None:
            exps.append(_("{} 형식").format(fmt))
    return line_dlm.join(exps)


def _request_dir(labfile, subdir):
    """요청된 서브디렉토리를 생성하고 경로를 반환.

    Args:
        labfile (str): 랩 파일 경로. None이면 현재 디렉토리 사용
        subdir (str): 생성할 서브디렉토리 이름

    Returns:
        str: 생성된 디렉토리의 절대 경로
    """
    if labfile is not None:
        adir = os.path.dirname(labfile)
    else:
        adir = os.getcwd()
    adir = os.path.join(adir, subdir)
    Path(adir).mkdir(parents=True, exist_ok=True)
    return adir


def download(url, filepath=None):
    """URL에서 파일을 다운로드.

    지정된 URL에서 파일을 다운로드하여 로컬에 저장함.
    파일 경로가 지정되지 않으면 URL의 마지막 부분을 파일명으로 사용.

    Args:
        url (str): 다운로드할 파일의 URL
        filepath (str, optional): 저장할 파일 경로. None이면 자동 생성

    Raises:
        requests.RequestException: 다운로드 실패시
    """
    if filepath is None:
        filepath = url.split("/")[-1]

    with open(filepath, "wb") as f:
        res = get(url)
        f.write(res.content)


def test_reset():
    """테스트 환경 초기화.

    테스트 디렉토리로 이동하고 이전 테스트에서 생성된
    임시 파일들을 모두 삭제함.
    """
    cwd = os.path.join(LOGLAB_HOME, "tests")
    os.chdir(cwd)

    # 기존 결과 삭제
    for f in glob("*.schema.json"):
        os.remove(f)
    for f in glob("*.txt"):
        os.remove(f)
    for f in glob("*.lab.json"):
        os.remove(f)
    for f in glob("*.html"):
        os.remove(f)


def absdir_for_html(adir):
    """HTML에서 사용할 수 있는 로컬 디렉토리 절대 경로로 변환.

    WSL 환경의 /mnt/드라이브 경로를 Windows file:// URL 형식으로 변환.

    Args:
        adir (str 또는 Path): 변환할 디렉토리 경로

    Returns:
        str: HTML에서 사용 가능한 절대 경로 또는 file:// URL
    """
    match = re.search(r"^/mnt/([a-z])/(.+)$", str(adir))
    if match is not None:
        drv, rdir = match.groups()
        drv = drv.upper()
        return f"file:///{drv}:/{rdir}"

    return adir
