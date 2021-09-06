"""LogLab 커맨드라인 툴."""
import os
import sys
from glob import glob

import click

from loglab.doc import text_from_labfile
from loglab.schema import verify_labfile, json_schema_from_labfile


_global_options = [
    click.option('--labfile', '-l', 'labfile', help='사용할 랩파일의 위치를 명시적으로 지정'),
]


def global_options(func):
    for option in reversed(_global_options):
        func = option(func)
    return func


def find_labfile(labfile, print_msg=True):
    """사용할 랩파일 디렉토리에서 찾기."""
    def through(labfile, print_msg):
        if not os.path.isabs(labfile):
            labfile = os.path.join(os.getcwd(), labfile)
        if print_msg:
            print(f"[사용할 랩파일 : {labfile}]")
        return labfile

    if labfile is not None:
        return through(labfile, print_msg)

    labs = glob("*.lab.json")
    num_labs = len(labs)
    if num_labs == 1:
        return through(labs[0], print_msg)
    elif num_labs == 0:
        print(f"Error: 현재 디렉토리에 랩파일이 없습니다. 새 랩파일을 "\
            "만들거나, 사용할 랩파일을 명시적으로 지정해 주세요.")
    else:
        print(f"Error: 현재 디렉토리에 랩파일이 하나 이상 있습니다. "\
            "사용할 랩파일을 명시적으로 지정해 주세요.")
    sys.exit(1)


@click.group()
def cli():
    pass


@cli.command()
@global_options
def doc(labfile):
    """로그 문서 표시."""
    labfile = find_labfile(labfile)
    labjs = verify_labfile(labfile)
    print(text_from_labfile(labjs))


@cli.command()
@global_options
def dummy(labfile):
    """가짜 로그 생성."""
    labfile = find_labfile(labfile)
    labjs = verify_labfile(labfile)
    click.echo("Generate Dummy Log Events")


@cli.command()
@global_options
def schema(labfile):
    """로그용 JSON 스키마 생성."""
    labfile = find_labfile(labfile)
    labjs = verify_labfile(labfile)
    print(json_schema_from_labfile(labjs))


@cli.command()
@global_options
def verify(labfile):
    """생성된 로그 파일 검증."""
    labfile = find_labfile(labfile)
    labjs = verify_labfile(labfile)
    click.echo("Verify Log Format.")


if __name__ == "__main__":
    cli(obj={})
