"""LogLab 커맨드라인 툴."""
import os
import sys
import json
import re

import click

from loglab.doc import text_from_labfile, html_from_labfile
from loglab.schema import verify_labfile, log_schema_from_labfile,\
    flow_schema_from_labfile, verify_logfile, handle_import
from loglab.util import find_labfile, find_log_schema, request_tmp_dir,\
    request_imp_dir, download
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
              help="긴 문자열 필링 않음")
def show(labfile, custom_type, name, keep_text):
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
    print(text_from_labfile(data, custom_type, name, keep_text))


@cli.command()
@click.argument('labfile', type=click.Path(exists=True))
@click.option('-c', '--custom-type', is_flag=True,
              help="커스텀 타입 그대로 출력")
@click.option('-o', '--output')
def html(labfile,  custom_type, output):
    """HTML 문서 출력."""
    # labfile = find_labfile(labfile)
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
    doc = html_from_labfile(data, kwargs, custom_type)
    if output is None:
        output = f"{domain['name']}.html"
    print(f"'{output}' 에 HTML 문서 저장.")
    with open(output, "wt", encoding='utf8') as f:
        f.write(doc)


@cli.command()
@click.argument('labfile', type=click.Path(exists=True))
def schema(labfile):
    """로그 및 플로우 파일용 스키마 생성."""
    labfile = find_labfile(labfile)
    data = verify_labfile(labfile)
    try:
        handle_import(labfile, data)
    except FileNotFoundError as e:
        print(f"Error: 가져올 파일 '{e}' 을 찾을 수 없습니다.")
        sys.exit(1)

    dname = data['domain']['name']
    log_scm_path = f'{dname}.log.schema.json'

    print(f"{log_scm_path} 에 로그 스키마 저장.")
    with open(log_scm_path, 'wt', encoding='utf8') as f:
        try:
            scm = log_schema_from_labfile(data)
            f.write(scm)
            json.loads(scm)
        except json.decoder.JSONDecodeError as e:
            print("Error: 생성된 JSON 스키마 에러. 로그랩 개발자에 문의 요망.")
            print(e)
            sys.exit(1)

    flow_scm_path = f'{dname}.flow.schema.json'
    print(f"{flow_scm_path} 에 플로우 스키마 저장.")
    with open(flow_scm_path, 'wt', encoding='utf8') as f:
        f.write(flow_schema_from_labfile(labfile, data))


@cli.command()
@click.argument('schema', type=click.Path())
@click.argument('logfile', type=click.Path(exists=True))
def verify(schema, logfile):
    """생성된 로그 파일 검증."""
    if not os.path.isfile(schema):
        print("Error: 로그 스키마를 찾을 수 없습니다. schema 명령으로 생성하거나, "
              "스키마의 경로를 옵션으로 지정하세요.")
        sys.exit(1)
    print(f"[로그 스키마 파일 : {schema}]")
    verify_logfile(schema, logfile)


@cli.command()
@click.argument('url')
@click.option('-o', '--output', help="저장할 파일명")
def fetch(url, output):
    """외부 랩 파일 다운로드."""
    edir = request_imp_dir()
    if output is None:
        output = url.split('/')[-1]
    if not output.endswith('.lab.json'):
        output += '.lab.json'
    path = os.path.join(edir, output)
    download(url, path)
    print(f"'{path} 에 저장.")


@cli.command()
def dummy():
    """가짜 로그 생성."""
    # labfile = find_labfile(labfile)
    verify_labfile(labfile)
    click.echo("Generate Dummy Log Events")


if __name__ == "__main__":
    click(obj={})
