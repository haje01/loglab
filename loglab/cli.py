"""LogLab 커맨드라인 툴."""

import codecs
import json
import re
import sys

import click

from loglab.doc import html_from_labfile, object_from_labfile, text_from_labfile
from loglab.model import handle_import
from loglab.schema import log_schema_from_labfile, verify_labfile, verify_logfile

# from loglab.util import download
from loglab.version import VERSION


@click.group(no_args_is_help=True)
def cli():
    """LogLab 메인 CLI 그룹.

    LogLab의 모든 명령어들을 그룹화하는 메인 진입점.
    """
    pass


@cli.command()
def version():
    """로그랩의 현재 버전을 표시.

    설치된 LogLab의 버전 정보를 출력함.
    """
    print(VERSION)


@cli.command()
@click.argument("labfile", type=click.Path(exists=True))
@click.option("-c", "--custom-type", is_flag=True, help="커스텀 타입 그대로 출력")
@click.option("-n", "--name", help="출력할 요소 이름 패턴")
@click.option(
    "-k", "--keep-text", is_flag=True, default=False, help="긴 문자열 그대로 출력"
)
@click.option("-l", "--lang", help="로그랩 메시지 언어")
def show(labfile, custom_type, name, keep_text, lang):
    """랩 파일의 내용을 텍스트 형태로 출력.

    lab 파일에 정의된 도메인, 타입, 베이스, 이벤트 등의 정보를
    사람이 읽기 쉬운 테이블 형태로 출력함.

    Args:
        labfile: 출력할 lab 파일 경로
        custom_type: 커스텀 타입 정보를 포함할지 여부
        name: 출력할 요소를 필터링할 정규식 패턴
        keep_text: 긴 문자열을 줄바꿈 없이 그대로 출력할지 여부
        lang: 출력 언어 코드
    """
    # labfile = find_labfile(labfile)
    data = verify_labfile(labfile)
    try:
        handle_import(labfile, data)
    except FileNotFoundError as e:
        print(f"Error: 가져올 파일 '{e}' 을 찾을 수 없습니다.")
        sys.exit(1)
    if name is not None:
        name = re.compile(name)
    print(text_from_labfile(data, custom_type, name, keep_text, lang))


@cli.command()
@click.argument("labfile", type=click.Path(exists=True))
@click.option("-c", "--custom-type", is_flag=True, help="커스텀 타입 그대로 출력")
@click.option("-o", "--output", help="출력 파일명")
@click.option("-l", "--lang", help="로그랩 메시지 언어")
def html(labfile, custom_type, output, lang):
    """랩 파일로부터 HTML 문서를 생성.

    lab 파일의 내용을 웹브라우저에서 보기 쉬운 HTML 형태로 변환하여
    파일로 저장. 생성된 HTML은 대화형 문서로 활용 가능.

    Args:
        labfile: 변환할 lab 파일 경로
        custom_type: 커스텀 타입 정보를 포함할지 여부
        output: 저장할 HTML 파일명. 지정하지 않으면 도메인명.html
        lang: 출력 언어 코드
    """
    data = verify_labfile(labfile)
    try:
        handle_import(labfile, data)
    except FileNotFoundError as e:
        print(f"Error: 가져올 파일 '{e}' 을 찾을 수 없습니다.")
        sys.exit(1)

    domain = data["domain"]
    kwargs = dict(domain=domain)
    doc = html_from_labfile(data, kwargs, custom_type, lang)
    if output is None:
        output = f"{domain['name']}.html"
    print(f"'{output}' 에 HTML 문서 저장.")
    with open(output, "wt", encoding="utf8") as f:
        f.write(doc)


@cli.command()
@click.argument("labfile", type=click.Path(exists=True))
def schema(labfile):
    """랩 파일로부터 로그 검증용 JSON 스키마를 생성.

    lab 파일에 정의된 이벤트들을 분석하여 실제 로그 파일의 유효성을
    검증할 수 있는 JSON Schema를 동적으로 생성함.

    Args:
        labfile: 스키마를 생성할 lab 파일 경로
    """
    data = verify_labfile(labfile)
    try:
        handle_import(labfile, data)
    except FileNotFoundError as e:
        print(f"Error: 가져올 파일 '{e}' 을 찾을 수 없습니다.")
        sys.exit(1)

    dname = data["domain"]["name"]
    scm_path = f"{dname}.schema.json"

    print(f"{scm_path} 에 로그 스키마 저장.")
    with open(scm_path, "wt", encoding="utf8") as f:
        try:
            scm = log_schema_from_labfile(data)
            f.write(scm)
            json.loads(scm)
        except json.decoder.JSONDecodeError as e:
            print("Error: 생성된 JSON 스키마 에러. 로그랩 개발자에 문의 요망.")
            print(e)
            sys.exit(1)


@cli.command()
@click.argument("schema", type=click.Path())
@click.argument("logfile", type=click.Path(exists=True))
def verify(schema, logfile):
    """실제 로그 파일이 스키마에 맞는지 검증.

    생성된 JSON Schema를 사용하여 JSON Lines 형태의 로그 파일이
    올바른 구조와 데이터 타입을 가지고 있는지 검증함.

    Args:
        schema: 검증에 사용할 JSON 스키마 파일 경로
        logfile: 검증할 로그 파일 경로
    """
    verify_logfile(schema, logfile)


@cli.command()
@click.argument("labfile", type=click.Path(exists=True))
@click.argument("code_type")
@click.option("-o", "--output", help="출력 파일명")
@click.option("-l", "--lang", help="로그랩 메시지 언어")
def object(labfile, code_type, output, lang):
    """랩 파일로부터 로그 작성용 코드 객체를 생성.

    lab 파일에 정의된 이벤트들을 지정된 프로그래밍 언어의
    클래스/구조체 코드로 변환. 생성된 코드는 로그 데이터를
    JSON Lines 형태로 직렬화하는 기능을 제공.

    Args:
        labfile: 코드를 생성할 lab 파일 경로
        code_type: 대상 언어 ('cs', 'py', 'cpp' 중 하나)
        output: 저장할 코드 파일명. 지정하지 않으면 표준 출력
        lang: 코드 내 메시지 언어 코드
    """
    data = verify_labfile(labfile)
    try:
        handle_import(labfile, data)
    except FileNotFoundError as e:
        print(f"Error: 가져올 파일 '{e}' 을 찾을 수 없습니다.")
        sys.exit(1)

    code_type = code_type.lower()
    if code_type not in ("cs", "py", "cpp"):
        print(f"Error: 지원하지 않는 코드 타입 (.{code_type}) 입니다.")
        sys.exit(1)

    src = object_from_labfile(data, code_type, lang)
    if output is None:
        print(src)
    else:
        with codecs.open(output, "w", "utf-8") as f:
            f.write(src)


if __name__ == "__main__":
    """CLI 스크립트로 직접 실행될 때의 진입점."""
    cli(obj={})
