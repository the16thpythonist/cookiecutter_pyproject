import os
import pathlib
import subprocess

PATH = pathlib.Path(__file__).parent.absolute()
PROJECT_PATH = os.path.dirname(PATH)


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
    proc = subprocess.run(cli_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    assert '--version' in proc.stdout.decode()

    # Since we gave the version in the context, we now require it to be in the
    version_command = f'{venv.python} -m pyproject.cli --version'
    proc = subprocess.run(version_command, stdout=subprocess.PIPE, shell=True)
    assert '0.2.0' in proc.stdout.decode()

    list_dir_command = f'{venv.python} -m pyproject.cli --list-dir'
    proc = subprocess.run(list_dir_command, stdout=subprocess.PIPE, shell=True)
    print(proc.stdout.decode())



def test_poetry(cookies, venv):
    context = {
        'directory_name': 'pyproject',
        'project_slug': 'pyproject',
        'version': '0.2.0'
    }
    result = cookies.bake(template=PROJECT_PATH, extra_context=context)

    # Most importantly there should be no error during the bake process
    assert result.exit_code == 0
    assert result.exception is None

    python_command = f'{venv.python} --version'
    proc = subprocess.run(python_command, stdout=subprocess.PIPE, shell=True)
    print('python version: ', proc.stdout.decode())
    assert proc.returncode == 0

    # We need to do a bit of a more complicated install here using poetry because this is the only way
    # how we can get the dev-dependencies installed as well.
    # But this has the added value that it also checks if the poetry installation works properly
    venv.install(f'poetry')
    poetry_path = os.path.join(venv.bin, 'poetry')

    # The following two commands are very important to correctly setup poetry with the virtualenv that
    # is being used for the testing here!
    poetry_config_command = f'{poetry_path} config virtualenvs.create false --local'
    proc = subprocess.run(poetry_config_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True, cwd=result.project_path)
    assert proc.returncode == 0

    poetry_env_command = f'{poetry_path} env use {venv.python}'
    proc = subprocess.run(poetry_env_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True, cwd=result.project_path)
    assert proc.returncode == 0

    # Here we install the project
    poetry_install_command = f'{poetry_path} install'
    proc = subprocess.run(poetry_install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True, cwd=result.project_path)
    assert proc.returncode == 0

    # Testing the "build" command
    poetry_build_command = f'{poetry_path} build'
    proc = subprocess.run(poetry_build_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True, cwd=result.project_path)
    assert proc.returncode == 0
    dist_path = os.path.join(result.project_path, 'dist')
    assert os.path.exists(dist_path)
    assert os.path.isdir(dist_path)
    assert len(os.listdir(dist_path)) != 0


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

    # We need to do a bit of a more complicated install here using poetry because this is the only way
    # how we can get the dev-dependencies installed as well.
    # But this has the added value that it also checks if the poetry installation works properly
    venv.install(f'poetry')
    poetry_path = os.path.join(venv.bin, 'poetry')

    poetry_config_command = f'{poetry_path} config virtualenvs.create false --local'
    proc = subprocess.run(poetry_config_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True, cwd=result.project_path)
    assert proc.returncode == 0

    poetry_env_command = f'{poetry_path} env use {venv.python} ; {poetry_path} env info'
    proc = subprocess.run(poetry_env_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True, cwd=result.project_path)
    assert proc.returncode == 0

    poetry_install_command = f'{poetry_path} install'
    proc = subprocess.run(poetry_install_command, stdout=subprocess.PIPE, shell=True, cwd=result.project_path)
    assert proc.returncode == 0

    pytest_path = os.path.join(venv.bin, 'pytest')
    assert os.path.exists(pytest_path)
    pytest_command = f'{pytest_path} -s {result.project_path}/tests'
    proc = subprocess.run(pytest_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    print(proc.stdout.decode(), proc.stderr.decode())
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

    # We need to do a bit of a more complicated install here using poetry because this is the only way
    # how we can get the dev-dependencies installed as well.
    # But this has the added value that it also checks if the poetry installation works properly
    venv.install(f'poetry')
    poetry_path = os.path.join(venv.bin, 'poetry')

    poetry_config_command = f'{poetry_path} config virtualenvs.create false --local'
    proc = subprocess.run(poetry_config_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True, cwd=result.project_path)
    assert proc.returncode == 0

    poetry_env_command = f'{poetry_path} env use {venv.python} ; {poetry_path} env info'
    proc = subprocess.run(poetry_env_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True, cwd=result.project_path)
    assert proc.returncode == 0

    poetry_install_command = f'{poetry_path} install'
    proc = subprocess.run(poetry_install_command, stdout=subprocess.PIPE, shell=True, cwd=result.project_path)
    assert proc.returncode == 0

    apidoc_command = f'{venv.bin}/sphinx-apidoc -f -o docs/source/ pyproject/'
    proc = subprocess.run(apidoc_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                          cwd=result.project_path)
    print(proc.stdout.decode(), proc.stderr.decode())
    print(os.listdir(f'{result.project_path}/docs'))
    assert proc.returncode == 0

    sphinx_command = f'{venv.bin}/sphinx-build -b html docs/ docs/_build/'
    proc = subprocess.run(sphinx_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                          cwd=result.project_path)
    print(proc.stdout.decode(), proc.stderr.decode())
    assert proc.returncode == 0



