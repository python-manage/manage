===============================
Click Manage
===============================


.. image:: https://img.shields.io/pypi/v/click_manage.svg
        :target: https://pypi.python.org/pypi/click_manage

.. image:: https://img.shields.io/travis/rochacbruno/click_manage.svg
        :target: https://travis-ci.org/rochacbruno/click_manage

.. image:: https://readthedocs.org/projects/click-manage/badge/?version=latest
        :target: https://click-manage.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://requires.io/github/rochacbruno/click_manage/requirements.svg?branch=master
        :target: https://requires.io/github/rochacbruno/click_manage/requirements?branch=master
        :alt: Dependencies


A "manage" command to add an interactive shell and commands support to your Python applications, based on click


* Free software: ISC license
* Documentation: https://click-manage.readthedocs.io.


Features
--------

With **click_manage** you add a commands manager to your Python project and
also it comes with an interactive shell with iPython support.

.. code-block:: console

    $ pip install click_manage
    $ cd /my_project_root_folder
    $ manage init
    creating manage.yml....

With that you now have a file **manage.yml** file describing how **manage** command should discovery your app modules and custom commands


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
