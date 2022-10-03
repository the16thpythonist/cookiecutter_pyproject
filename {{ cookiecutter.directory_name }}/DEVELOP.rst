======================
Development Cheatsheet
======================

Git
===

Add Package Remote
------------------

It makes sense to directly supply a Github personal auth token when registering a new remote location for
the local repository, because that will remove any hassle with authentication when trying to push in the
future.

.. code-block:: shell

    git remote add origin https:://[github_username]:[github_token]@github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
    git push origin master


Poetry
======

Package Release on PyPI
-----------------------

The following steps in preparation of pushing a new release to github and PyPi. All references to the
version string will automatically be updated by the ``version`` command. Note that it is important to use
single quotes for the ``publish`` command.

.. code-block:: shell

    poetry lock
    poetry version [ major | minor | patch ]
    poetry build
    poetry publish --username='[pypi username]' --password='[pypi password]'
    git commit -a -m "commit message"
    git commit origin master


Sphinx
======

Create the documentation
------------------------

First you want to compile all of the docstrings with ``sphinx-autodoc`` and then build the html
documentation like this:

.. code-block:: shell

    sphinx-apidoc -f -o docs/source ./
    sphinx-build -b html docs docs/_build
