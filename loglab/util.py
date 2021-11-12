"""유틸리티 모음."""
import os
import sys
import re
from glob import glob
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlparse
from pathlib import Path
from glob import glob

from requests import get
import gettext

LOGLAB_HOME = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
BUILTIN_TYPES = ('string', 'integer', 'number', 'boolean', 'datetime')

lc_dir = os.path.join(LOGLAB_HOME, 'locales')


def get_translator(lang):
    if lang is None:
        return lambda x: x
    trans = gettext.translation('base', localedir=lc_dir, languages=(lang,))
    return trans.gettext


def get_dt_desc(lang):
    _ = get_translator(lang)
    return _("이벤트 일시")


def get_object_warn(lang):
    _ = get_translator(lang)
    return _("이 파일은 LogLab 에서 생성된 것입니다. 고치지 마세요!")


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
        with open(path, 'rt', encoding='utf8') as f:
            return f.read()


# def _init_fields():
#     fields = {}
#     fields["DateTime"] = ["datetime", EDT_DESC]
#     return fields


def explain_rstr(f, lang, line_dlm='\n'):
    """제약을 설명으로 변환."""
    _ = get_translator(lang)
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
            if len(enum) > 0:
                expl = []
                for d in enum:
                    if type(d) is list:
                        expl.append(f"{d[0]} ({d[1]})")
                    else:
                        expl.append(str(d))
                enum = expl
            arr = ', '.join(expl)
            enum = _("{} 중 하나").format(arr)

        assert amin is None or xmin is None,\
            'minimum 과 exclusiveMinimum 함께 사용 불가'
        assert amax is None or xmax is None,\
            'maximum 과 exclusiveMaximum 함께 사용 불가'

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
            stmts.append(_("{} 자 이상").format(minl))
        if maxl is not None:
            stmts.append(_("{} 자 이하").format(maxl))
        if len(stmts) > 0:
            exps.append(' '.join(stmts))

        if enum is not None:
            if type(enum[0]) is list:
                _enum = []
                for i, d in enum:
                    _enum.append(f'{i} ({d})')
                enum = _enum
            arr = ', '.join(enum)
            exps.append(_("{} 중 하나").format(arr))
        if ptrn is not None:
            exps.append(_("정규식 {} 매칭").format(ptrn))
        if fmt is not None:
            exps.append(_("{} 형식").format(fmt))
    return line_dlm.join(exps)


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
    """HTML 용 로컬 디렉토리 절대 경로."""
    match = re.search(r'^/mnt/([a-z])/(.+)$', str(adir))
    if match is not None:
        drv, rdir = match.groups()
        drv = drv.upper()
        return f'file:///{drv}:/{rdir}'

    return adir
