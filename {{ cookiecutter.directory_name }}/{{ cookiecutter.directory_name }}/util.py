import os
import pathlib
import logging

import jinja2 as j2

PATH = pathlib.Path(__file__).parent.absolute()
VERSION_PATH = os.path.join(PATH, 'VERSION')
TEMPLATES_PATH = os.path.join(PATH, 'templates')

# Use this jinja environment to access the templates defined in j2
TEMPLATE_ENV = j2.Environment(
    loader=j2.FileSystemLoader(TEMPLATES_PATH),
    autoescape=j2.select_autoescape()
)

# You can use this logger as a default argument for functions which may optionally use a logger! It can be
# used like any other logger but doesn't actually log anything.
NULL_LOGGER = logging.getLogger('NULL')
NULL_LOGGER.addHandler(logging.NullHandler())


def get_version() -> str:
    """
    Returns the version string which is saved in the VERSION file within the package's main folder.

    :return str: the version string
    """
    with open(VERSION_PATH, mode='r') as file:
        content = file.read()
        return content.replace(' ', '').replace('\n', '')
