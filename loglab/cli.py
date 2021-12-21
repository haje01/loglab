"""LogLab 커맨드라인 툴."""
import sys
import json
import re
import codecs

import click

from loglab.doc import text_from_labfile, html_from_labfile,\
    object_from_labfile
from loglab.schema import verify_labfile, log_schema_from_labfile,\
    verify_logfile
from loglab.model import handle_import
# from loglab.util import download
from loglab.version import VERSION


@click.group()
def cli():
    pass


@cli.command()
def version():
    """로그랩 버전 표시."""
    print(VERSION)


@cli.command()
@click.argument('labfile', type=click.Path(exists=True))
@click.option('-c', '--custom-type', is_flag=True,
              help="커스텀 타입 그대로 출력")
@click.option('-n', '--name', help="출력할 요소 이름 패턴")
@click.option('-k', '--keep-text', is_flag=True, default=False,
              help="긴 문자열 그대로 출력")
@click.option('-l', '--lang', help="로그랩 메시지 언어")
def show(labfile, custom_type, name, keep_text, lang):
    """로그 구성 요소 출력."""
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
@click.argument('labfile', type=click.Path(exists=True))
@click.option('-c', '--custom-type', is_flag=True,
              help="커스텀 타입 그대로 출력")
@click.option('-o', '--output', help="출력 파일명")
@click.option('-l', '--lang', help="로그랩 메시지 언어")
def html(labfile,  custom_type, output, lang):
    """HTML 문서 출력."""
    data = verify_labfile(labfile)
    try:
        handle_import(labfile, data)
    except FileNotFoundError as e:
        print(f"Error: 가져올 파일 '{e}' 을 찾을 수 없습니다.")
        sys.exit(1)

    domain = data['domain']
    kwargs = dict(
        domain=domain
    )
    doc = html_from_labfile(data, kwargs, custom_type, lang)
    if output is None:
        output = f"{domain['name']}.html"
    print(f"'{output}' 에 HTML 문서 저장.")
    with open(output, "wt", encoding='utf8') as f:
        f.write(doc)


@cli.command()
@click.argument('labfile', type=click.Path(exists=True))
def schema(labfile):
    """로그 및 플로우 파일용 스키마 생성."""
    data = verify_labfile(labfile)
    try:
        handle_import(labfile, data)
    except FileNotFoundError as e:
        print(f"Error: 가져올 파일 '{e}' 을 찾을 수 없습니다.")
        sys.exit(1)

    dname = data['domain']['name']
    scm_path = f'{dname}.schema.json'

    print(f"{scm_path} 에 로그 스키마 저장.")
    with open(scm_path, 'wt', encoding='utf8') as f:
        try:
            scm = log_schema_from_labfile(data)
            f.write(scm)
            json.loads(scm)
        except json.decoder.JSONDecodeError as e:
            print("Error: 생성된 JSON 스키마 에러. 로그랩 개발자에 문의 요망.")
            print(e)
            sys.exit(1)


@cli.command()
@click.argument('schema', type=click.Path())
@click.argument('logfile', type=click.Path(exists=True))
def verify(schema, logfile):
    """생성된 로그 파일 검증."""
    verify_logfile(schema, logfile)


@cli.command()
@click.argument('labfile', type=click.Path(exists=True))
@click.argument('code_type')
@click.option('-o', '--output', help="출력 파일명")
@click.option('-l', '--lang', help="로그랩 메시지 언어")
def object(labfile, code_type, output, lang):
    """로그 객체 코드 출력."""
    data = verify_labfile(labfile)
    try:
        handle_import(labfile, data)
    except FileNotFoundError as e:
        print(f"Error: 가져올 파일 '{e}' 을 찾을 수 없습니다.")
        sys.exit(1)

    code_type = code_type.lower()
    if code_type not in ('cs', 'py'):
        print(f"Error: 지원하지 않는 코드 타입 (.{code_type}) 입니다.")
        sys.exit(1)

    src = object_from_labfile(data, code_type, lang)
    if output is None:
        print(src)
    else:
        with codecs.open(output, 'w', 'utf-8') as f:
            f.write(src)


if __name__ == "__main__":
    cli(obj={})
