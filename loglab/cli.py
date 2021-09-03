"""LogLab 커맨드라인 툴."""
import click

from loglab.doc import text_from_meta


@click.group()
@click.option('-m', '--meta', help="Path of a meta file.")
@click.pass_context
def main(ctx, meta):
    """Click Entry."""
    ctx.ensure_object(dict)
    ctx.obj['meta'] = meta


@main.command()
@click.pass_context
def doc(ctx):
    """로그 문서 생성."""
    meta_path = ctx.obj['meta']
    assert meta_path is not None
    print(text_from_meta(meta_path))


@main.command()
@click.pass_context
def sample(ctx):
    """가짜 로그 생성."""
    click.echo("Generate Pseudo Log Events")


@main.command()
@click.pass_context
def schema(ctx):
    """JSON 스키마 파일 생성."""
    click.echo("Generate JSON Schema File.")


@main.command()
@click.pass_context
def verify(ctx):
    """로그 파일 검증."""
    click.echo("Verify Log Format.")


if __name__ == "__main__":
    cli(obj={})
