===============================
Manage
===============================


.. image:: https://img.shields.io/pypi/v/manage.svg
        :target: https://pypi.python.org/pypi/manage

.. image:: https://img.shields.io/travis/rochacbruno/manage.svg
        :target: https://travis-ci.org/rochacbruno/manage

.. image:: https://readthedocs.org/projects/manage/badge/?version=latest
        :target: https://manage.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://requires.io/github/rochacbruno/manage/requirements.svg?branch=master
        :target: https://requires.io/github/rochacbruno/manage/requirements?branch=master
        :alt: Dependencies


A "manage" command to add an interactive shell and commands support to your Python applications, based on click


* Free software: ISC license
* Documentation: https://manage.readthedocs.io.


Features
--------

With **manage** you add a commands manager to your Python project and
also it comes with an interactive shell with iPython support.

.. code-block:: console

    $ pip install manage
    $ cd /my_project_root_folder
    $ manage init
    creating manage.yml....

With that you now have a file **manage.yml** file describing how **manage** command should discover your app modules and custom commands

The Shell
---------

By default the command :code:`manage shell` is included, it is a simple Python REPL console with some
configurable options.

You can change the banner message to say anything you want, e.g: "Welcome to my shell!" and you can also
specify some objects to be automatically imported in to the shell context so when you enter in to the shell you
already have your project's common objects available.

Also you can specify a custom function to run or a string based code block to run, useful to init and configure the objects.

If **IPython** is installed it will use it, otherwise will use the default Python console including support for tab autocomplete.

Check the example in: https://github.com/rochacbruno/manage/tree/master/examples/simple


Custom Commands
---------------


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
