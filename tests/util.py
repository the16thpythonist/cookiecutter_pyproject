import os
import pathlib
import subprocess
import typing as t

from pytest_venv import VirtualEnvironment

PATH = pathlib.Path(__file__).parent.absolute()
PROJECT_PATH = os.path.dirname(PATH)


def run_command(command: str,
                cwd: t.Optional[str] = None,
                ) -> t.Tuple[subprocess.CompletedProcess, str, str]:
    proc = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd
    )
    out = proc.stdout.decode()
    err = proc.stderr.decode()

    return proc, out, err


def prepare_poetry(project_path: str,
                   venv: VirtualEnvironment,
                   do_prepare: bool = False
                   ) -> t.Tuple[str, str]:

    # First of all we need to install poetry into the venv
    venv.install('poetry')
    poetry = f'{venv.python} -m poetry'

    if do_prepare:
        cache_path = os.path.join(project_path, '.cache')
        envs_path = os.path.join(cache_path, 'virtualenvs', 'envs.toml')
        os.makedirs(os.path.dirname(envs_path), exist_ok=True)
        with open(envs_path, mode='w') as file:
            file.write(' ')

        run_command(f'{poetry} config cache-dir {cache_path} --local', cwd=project_path)
        run_command(f'{poetry} config virtualenvs.create false --local', cwd=project_path)

    # and we also need to make sure to switch to the correct environment
    run_command(f'{poetry} env use {venv.python}', cwd=project_path)
    run_command(f'{poetry} --no-cache install', cwd=project_path)

    return poetry, project_path