import os
import pathlib
import subprocess
import shutil

from .util import PATH, PROJECT_PATH
from .util import run_command
from .util import prepare_poetry


def test_bake(cookies):
    """
    Tests if the cookiecutter command basically runs without error and whether all the files are present
    in the created folder.
    """
    context = {
        'directory_name': 'pyproject',
        'project_slug': 'pyproject'
    }
    result = cookies.bake(template=PROJECT_PATH, extra_context=context)

    # Most importantly there should be no error during the bake process
    assert result.exit_code == 0
    assert result.exception is None

    # Then we check the relevant files exist
    files = os.listdir(result.project_path)
    assert 'README.rst' in files
    assert 'DEVELOP.rst' in files
    assert 'HISTORY.rst' in files
    assert 'pyproject.toml' in files
    assert 'pyproject' in files
    assert 'tests' in files

    package_path = os.path.join(result.project_path, 'pyproject')
    package_files = os.listdir(package_path)
    assert 'util.py' in package_files
    assert 'cli.py' in package_files
    assert 'VERSION' in package_files


def test_installation(cookies, venv):
    """
    Tests whether the templated folder can be installed by pip. Also tests if the CLI works for example
    """
    context = {
        'directory_name': 'pyproject',
        'project_slug': 'pyproject',
        'version': '0.2.0'
    }
    result = cookies.bake(template=PROJECT_PATH, extra_context=context)

    # Most importantly there should be no error during the bake process
    assert result.exit_code == 0
    assert result.exception is None

    # ~ TESTING INSTALLATION
    # Now we attempt to install this into a new virtualenv
    venv.install(f'{result.project_path}')

    # ~ TESTING CLI
    # After it has been installed into a venv we can attempt to use it
    cli_command = f'{venv.python} -m pyproject.cli --help'
    # We know that if the help command goes through "--version" definitely needs to be in there
    proc, out, err = run_command(cli_command)
    assert '--version' in proc.stdout.decode()

    # Since we gave the version in the context, we now require it to be in the
    version_command = f'{venv.python} -m pyproject.cli --version'
    proc, out, err = run_command(version_command)
    assert '0.2.0' in proc.stdout.decode()


def test_poetry(cookies, venv):
    context = {
        'directory_name': 'pyproject',
        'project_slug': 'pyproject',
        'version': '0.3.0'
    }
    result = cookies.bake(template=PROJECT_PATH, extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None

    # First of all we need to install poetry into the venv
    venv.install('poetry==1.2.1')
    poetry_path = f'{venv.python} -m poetry'

    # and we also need to make sure to switch to the correct environment
    env_command = f'{poetry_path} -vvv env use {venv.python}'
    proc, out, err = run_command(env_command, cwd=result.project_path)
    # Then we need to run "poetry install"
    install_command = f'{poetry_path} --no-cache install'
    proc, out, err = run_command(install_command, cwd=result.project_path)
    assert proc.returncode == 0
    assert 'No dependencies to install or update' not in out

    # We can check if that worked by attempting to import "click" first (which is a dependency of our
    # project and thus should have been installed and then also attempting to install our project itself
    proc, out, err = run_command(f'{venv.python} -c "import click"')
    assert proc.returncode == 0
    proc, out, err = run_command(f'{venv.python} -c "import pyproject"')
    assert proc.returncode == 0

    # Now another thingy we can test is if the poetry bumpversion feature works
    bumpversion_command = f'{poetry_path} version minor'
    proc, out, err = run_command(bumpversion_command, cwd=result.project_path)
    assert proc.returncode == 0
    proc, out, err = run_command(install_command, cwd=result.project_path)
    assert proc.returncode == 0

    cli_path = os.path.join(venv.bin, 'pyproject')
    assert os.path.exists(cli_path)
    version_command = f'{cli_path} --version'
    proc, out, err = run_command(version_command)
    assert proc.returncode == 0
    assert '0.3.0' in out


def test_unittests(cookies, venv):
    context = {
        'directory_name': 'pyproject',
        'project_slug': 'pyproject',
        'version': '0.2.0'
    }
    result = cookies.bake(template=PROJECT_PATH, extra_context=context)

    # Most importantly there should be no error during the bake process
    assert result.exit_code == 0
    assert result.exception is None

    poetry, path = prepare_poetry(result.project_path, venv)

    # First we check if pytest is even available for the venv binary
    pytest_command = f'{venv.python} -c "import pytest"'
    proc, out, err = run_command(pytest_command)
    assert proc.returncode == 0

    # Then we can actually run pytest for the tests inside the project folder
    tests_path = os.path.join(path, 'tests')
    test_command = f'{venv.python} -m pytest -s {tests_path}'
    proc, out, err = run_command(test_command)
    assert proc.returncode == 0


def test_documentation(cookies, venv):
    context = {
        'directory_name': 'pyproject',
        'project_slug': 'pyproject',
        'version': '0.2.0'
    }
    result = cookies.bake(template=PROJECT_PATH, extra_context=context)

    # Most importantly there should be no error during the bake process
    assert result.exit_code == 0
    assert result.exception is None

    poetry, path = prepare_poetry(result.project_path, venv)

    apidoc_command = f'{venv.bin}/sphinx-apidoc -f -o docs/source/ pyproject/'
    proc, out, err = run_command(apidoc_command, cwd=path)
    assert proc.returncode == 0

    docs_build_path = os.path.join(path, 'docs', '_build')
    shutil.rmtree(docs_build_path, True)
    assert not os.path.exists(docs_build_path)

    sphinx_command = f'{venv.bin}/sphinx-build -b html ./docs/ ./docs/_build/'
    proc, out, err = run_command(sphinx_command, cwd=path)
    print(out)
    print(err)
    assert proc.returncode == 0
    assert os.path.exists(docs_build_path)
    assert len(os.listdir(docs_build_path)) != 0



