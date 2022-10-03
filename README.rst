|made-with-python| |python-version| |version|

.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/

.. |python-version| image:: https://img.shields.io/badge/Python-3.8.0-green.svg
   :target: https://www.python.org/

.. |version| image:: https://img.shields.io/badge/version-{{ cookiecutter.version }}-orange.svg
   :target: https://www.python.org/

===========================
Cookiecutter Python Project
===========================

This is a *yet another* cookiecutter_ for python projects :grin:! It mainly differs in the same way any
such cookiecutter differs: It is less bloated in some areas while being a bit more extensive in others.

These are the main features:

* Modern package management using Poetry_ and ``pyproject.toml``
    * Using poetry-bumpversion_ for easy version management
* Ready-to-go Click_ command line interface as a ``CommandGroup`` unlike one simple ``Command`` as it
  is usually done.
    * Uses custom ``CommandGroup`` subclass, which makes extensive customizations such as lazy loading of
      commands or a plugin system easier in the future.
    * ``--version`` optional already implemented and fully integrated into automatic *bumpversion*
      version management
* Sphinx_ documentation with ReadTheDocs_ theme and sphinx-autodoc_ pre-configured


Usage
=====

You need ``cookiecutter`` installed to use this package:

.. code-block:: shell

    cookiecutter https://github.com/the16thpythonist/cookiecutter_pyproject.git


.. _cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _Poetry: https://python-poetry.org/
.. _poetry-bumpversion: https://github.com/monim67/poetry-bumpversion
.. _Click: https://click.palletsprojects.com/en/8.1.x/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _sphinx-autodoc: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
.. _ReadTheDocs: https://readthedocs.org/
