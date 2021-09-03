"""LogLab 커맨드라인 툴."""
import os
import sys
from glob import glob

import click

from loglab.doc import text_from_labfile
from loglab.util import verify_labfile


_global_options = [
    click.option('--labfile', '-l', 'labfile', help='사용할 랩파일의 위치를 명시적으로 지정'),
]


def global_options(func):
    for option in reversed(_global_options):
        func = option(func)
    return func


def check_labfile(labfile):
    if labfile is not None:
        return labfile

    labs = glob("*.lab.json")
    num_labs = len(labs)
    if num_labs == 1:
        return labs[0]
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
def verify(labfile):
    """랩파일 검증."""
    verify_labfile(labfile)


@cli.command()
@global_options
def doc(labfile):
    """로그 문서 표시."""
    labfile = check_labfile(labfile)
    labjs = verify_labfile(labfile)
    print(text_from_labfile(labjs))


@cli.command()
@global_options
def dummy(labfile):
    """가짜 로그 생성."""
    labfile = check_labfile(labfile)
    click.echo("Generate Dummy Log Events")


@cli.command()
@global_options
def schema(labfile):
    """JSON 스키마 파일 생성."""
    labfile = check_labfile(labfile)
    click.echo("Generate JSON Schema File.")


@cli.command()
@global_options
def verify(labfile):
    """로그 파일 검증."""
    labfile = check_labfile(labfile)
    click.echo("Verify Log Format.")


if __name__ == "__main__":
    cli(obj={})
