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

With that you now have a file **manage.yml** file describing how **manage** command should discovery your app modules and custom commands


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
