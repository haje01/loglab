"""LogLab 커맨드라인 툴."""
import os
import sys
import json

import click

from loglab.show import text_from_labfile
from loglab.schema import verify_labfile, log_schema_from_labfile,\
    flow_schema_from_labfile, verify_logfile
from loglab.util import find_labfile, find_log_schema
from loglab.version import VERSION


_global_options = [
    click.option('--labfile', '-l', 'labfile',
                 help='사용할 랩파일의 위치를 명시적으로 지정'),
]


def global_options(func):
    for option in reversed(_global_options):
        func = option(func)
    return func


@click.group()
def cli():
    pass


@cli.command()
def version():
    """로그랩 버전 표시."""
    print(VERSION)


@cli.command()
@global_options
def show(labfile):
    """로그 구조 출력."""
    labfile = find_labfile(labfile)
    labjs = verify_labfile(labfile)
    print(text_from_labfile(labjs))


@cli.command()
@global_options
def schema(labfile):
    """로그 및 플로우 파일용 스키마 생성."""
    labfile = find_labfile(labfile)
    labjs = verify_labfile(labfile)
    prj_dir = os.path.dirname(labfile)
    prj_name = labjs['domain']['name']
    log_scm_path = os.path.join(prj_dir, prj_name + ".log.schema.json")

    print(f"'{log_scm_path} 에 로그 스키마 저장.")
    with open(log_scm_path, 'wt') as f:
        try:
            scm = log_schema_from_labfile(labjs)
            f.write(scm)
            json.loads(scm)
        except json.decoder.JSONDecodeError as e:
            print("Error: 생성된 JSON 스키마 에러. 로그랩 개발자에 문의 요망.")
            print(e)
            sys.exit(1)

    flow_scm_path = os.path.join(prj_dir, prj_name + ".flow.schema.json")
    print(f"'{flow_scm_path} 에 플로우 스키마 저장.")
    with open(flow_scm_path, 'wt') as f:
        f.write(flow_schema_from_labfile(labfile, labjs))


@cli.command()
@global_options
@click.argument('logfile')
@click.option('-s', '--schema', help="로그 스키마 경로")
def verify(labfile, logfile, schema):
    """생성된 로그 파일 검증."""
    labfile = find_labfile(labfile)
    labjs = verify_labfile(labfile)
    schema = find_log_schema(labjs, schema)
    if schema is None:
        print("Error: 로그 스키마를 찾을 수 없습니다. schema 명령으로 생성하거나, "
              "스키마의 경로를 옵션으로 지정하세요.")
        sys.exit(1)
    print(f"[사용할 스키마 파일 : {schema}]")
    verify_logfile(schema, logfile)


@cli.command()
@global_options
def dummy(labfile):
    """가짜 로그 생성."""
    labfile = find_labfile(labfile)
    verify_labfile(labfile)
    click.echo("Generate Dummy Log Events")


if __name__ == "__main__":
    cli(obj={})
