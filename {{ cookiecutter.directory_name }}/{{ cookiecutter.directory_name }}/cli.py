import os
import click
import typing as t

from {{ cookiecutter.directory_name }}.util import PATH
from {{ cookiecutter.directory_name }}.util import get_version


class Group(click.Group):
    """
    Custom implementation of click command group.

    You will probably not need this in most cases, but if you do it is good to have it. The main use case
    of having a custom class for this is for "lazy loading" commands. That means some commands to be created
    dynamically at runtime rather than statically in the code. The most common use case for that is
    probably plugin support for your application.
    """
    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        # At this point in the constructor you should be setting up / gaining access to a plugin manager
        # or something similar.

    def list_commands(self, ctx: click.Context) -> t.List[str]:
        # Write some custom code here that queries the plugin manager and injects the additional command
        # names into the list to be returned
        return super(Group, self).list_commands(ctx)

    def get_command(self, ctx: click.Context, cmd_name: str) -> t.Optional[click.Command]:
        # Write some custom code here that dynamically assembles / retrieves the new custom command
        # dynamically
        return super(Group, self).get_command(ctx, cmd_name)


@click.group('{{ cookiecutter.project_slug }}', invoke_without_command=True, cls=Group)
@click.option('--version', is_flag=True, help='Prints the version of the package')
@click.option('--list-dir', is_flag=True,
              help='Development option. Prints the contents of the package folder')
@click.pass_context
def cli(ctx: click.Context,
        version: bool,
        list_dir: bool):

    # "ctx.obj" is a storage space that we can use to pass custom states / objects between the different
    # command levels. With this we pass the Group object along, but usually you want this to be a config
    # singleton or something similar that keeps track of your global application state.
    ctx.obj = ctx.command

    if version:
        click.secho(get_version())
        return

    if list_dir:
        path = os.path.dirname(PATH)
        click.secho(path)
        click.secho(os.listdir(path))


# cli.add_command(...)


if __name__ == '__main__':
    cli()