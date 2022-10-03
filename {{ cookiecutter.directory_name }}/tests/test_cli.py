import click
from click.testing import CliRunner

from {{ cookiecutter.directory_name }}.cli import cli

from .util import LOG


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    LOG.info(result.output)
    assert result.exit_code == 0
    assert len(result.output) != 0


def test_list_dir():
    runner = CliRunner()
    result = runner.invoke(cli, ['--list-dir'])
    LOG.info(result.output)
    assert result.exit_code == 0
    assert len(result.output) != 0

