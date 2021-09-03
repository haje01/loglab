"""LogLab 커맨드라인 툴."""
import os
import sys
from glob import glob

import click

from loglab.doc import text_from_labfile

_global_options = [
    click.option('--labfile', '-l', 'labfile', help='사용할 랩파일의 위치를 명시적으로 지정'),
]

def global_options(func):
    for option in reversed(_global_options):
        func = option(func)
    return func


@click.group()
def main():
    pass


def check_labfile(labfile):
    if labfile is not None:
        return

    labs = glob("*.labfile.json")
    num_labs = len(labs)
    if num_labs == 0:
        print(f"Error: 현재 디렉토리에 랩파일이 없습니다. 새 랩파일을 "\
            "만들거나, 사용할 랩파일을 명시적으로 지정해 주세요.")
    if num_labs > 0:
        print(f"Error: 현재 디렉토리에 랩파일이 하나 이상 있습니다. "\
            "사용할 랩파일을 명시적으로 지정해 주세요.")
    sys.exit(1)


@main.command()
@global_options
def doc(labfile):
    """로그 문서 표시."""
    check_labfile(labfile)
    print(text_from_labfile(labfile))


@main.command()
@global_options
def sample(labfile):
    """가짜 로그 생성."""
    check_labfile(labfile)
    click.echo("Generate Pseudo Log Events")


@main.command()
@global_options
def schema(labfile):
    """JSON 스키마 파일 생성."""
    check_labfile(labfile)
    click.echo("Generate JSON Schema File.")


@main.command()
@global_options
def verify(labfile):
    """로그 파일 검증."""
    check_labfile(labfile)
    click.echo("Verify Log Format.")


if __name__ == "__main__":
    cli(obj={})
