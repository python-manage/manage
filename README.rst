======
Manage
======
------------------------------------------------------------
Command Line Manager + Interactive Shell for Python Projects
------------------------------------------------------------

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


* Free software: ISC license
* Documentation: https://manage.readthedocs.io.


Features
========

With **manage** you add a **command line manager** to your Python project and
also it comes with an interactive shell with iPython support.

All you have to do is **init** your project directory (creating the manage.yml file)

.. code-block:: console

    $ pip install manage
    $ cd /my_project_root_folder
    $ manage init
    creating manage.yml....

The file **manage.yml** describes how **manage** command should discover your app modules and custom commands and also it
defines which objects should be loaded in to the **shell**

.. note::

   Windows users may need to install proper version of PyYAML depending on the version of that thing you call an operating system,
   installable available in: https://pypi.python.org/pypi/PyYAML
   **or consider using Linux and don't worry about this as everything works well in Linux except games, photoshop and solitary game :)**

The Shell
=========

By default the command :code:`manage shell` is included, it is a simple Python REPL console with some
configurable options.

You can change the banner message to say anything you want, **e.g: "Welcome to my shell!"** and you can also
specify some objects to be automatically imported in to the shell context so when you enter in to the shell you
already have your project's common objects available.

Also you can specify a custom function to run or a string based code block to run, useful to init and configure the objects.

Consoles

:code:`manage shell` can start different consoles by passing the options

- :code:`manage shell --ipython`  - This is the default (if ipython installed)
- :code:`manage shell --ptpython`
- :code:`manage shell --bpython`
- :code:`manage shell --python` - This is the **default Python console** including support for autocomplete. (will be default when no other is installed)

The first thing you can do with **manage** is customizing the objects that will be automatically loaded in to shell,
saving you from importing and initializing a lot of stuff every time you need to play with your app via console.

Edit **manage.yml** with:

.. code-block:: yaml

    project_name: My Awesome Project
    help_text: |
      This is the {project_name} interactive shell!
    shell:
      console: bpython
      readline_enabled: true
      banner:
        enabled: true
        message: 'Welcome to {project_name} shell!'
      auto_import:
        display: true
        objects:
          my_system.config.settings:
          my_system.my_module.MyClass:
          my_system.my_module.OtherClass:
            as: NiceClass
          sys.path:
            as: sp
            init:
              insert:
                args:
                  - 0
                  - /path/to/be/added/automatically/to/sys/path
      init_script: |
        from my_system.config import settings
        print("Initializing settings...")
        settings.configure()


Then the above **manage.yaml** will give you a shell like this:

.. code-block:: console

    $ manage shell
    Initializing settings...
    Welcome to My Awesome Project shell!
        Auto imported: ['sp', 'settings', 'MyClass', 'NiceCLass']
    >>>  NiceClass. <tab> # autocomplete enabled


Check more examples in:

https://github.com/rochacbruno/manage/tree/master/examples/

The famous **naval fate** example (used in docopt and click) is in:

https://github.com/rochacbruno/manage/tree/master/examples/naval/


Custom Commands
===============

Sometimes you need to add custom commands in to your project
e.g: A command to add users to your system::

  $ manage create_user --name=Bruno --passwd=1234
  Creating the user...

**manage** has some different ways for you to define custom commands,
you can use **click commands** defined in your project modules,
you can also use **function_commands** defined anywhere in your project,
and if really needed can define **inline_commands** inside the **manage.yml** file

1. Using a custom click_commands module (single file)
-----------------------------------------------------

Lets say you have a commands module in your application, you write your custom command there and **manage** will load it

.. code-block:: python

  # myproject/commands.py
  import click
  @click.command()
  @click.option('--name')
  @click.option('--passwd')
  def create_user(name, passwd):
      """Create a new user"""
      click.echo('Creating the user...')
      mysystem.User.create(name, password)


Now you go to your **manage.yml** or **.manage.yml** and specify your custom command module.

.. code-block:: yaml

  click_commands:
    - module: commands

Now you run **manage --help**

.. code-block:: console

  $ manage --help
  ...
  Commands:
    create_user  Create a new user
    debug        Shows the parsed manage file
    init         Initialize a manage shell in current...
    shell        Runs a Python shell with context


Using a click_commands package (multiple files)
-----------------------------------------------

It is common to have different files to hold your commands so you may prefer having
a **commands/** package and some **python** modules inside it to hold commands.

.. code-block:: python

  # myproject/commands/user.py
  import click
  @click.command()
  @click.option('--name')
  @click.option('--passwd')
  def create_user(name, passwd):
      """Create a new user"""
      click.echo('Creating the user...')
      mysystem.User.create(name, password)

.. code-block:: python

  # myproject/commands/system.py
  import click
  @click.command()
  def clear_cache():
      """Clear the system cache"""
      click.echo('The cache will be erased...')
      mysystem.cache.clear()

So now you want to add all those commands to your **manage** editing your manage file with.

.. code-block:: yaml

  click_commands:
    - module: commands

Now you run **manage --help**  and you have commands from both modules

.. code-block:: console

  $ manage --help
  ...
  Commands:
    create_user  Create a new user
    clear_cache  Clear the system cache
    debug        Shows the parsed manage file
    init         Initialize a manage shell in current...
    shell        Runs a Python shell with context

Custom click_command names
--------------------------

Sometimes the name of commands differ from the name of the function so you can
customize it.

.. code-block:: yaml

  click_commands:
    - module: commands.system
      config:
        clear_cache:
          name: reset_cache
          help_text: This resets the cache
    - module: commands.user
      config:
        create_user:
          name: new_user
          help_text: This creates new user

Having different namespaces
---------------------------

If customizing the name looks too much work for you, and you are only trying to handle naming conflicts
you can user namespaced commands.

.. code-block:: yaml

  namespaced: true
  click_commands:
    - module: commands

Now you run **manage --help** and you can see all the commands in the same module will be namespaced by **modulename_**

.. code-block:: console

  $ manage --help
  ...
  Commands:
    user_create_user    Create a new user
    system_clear_cache  Clear the system cache
    debug        Shows the parsed manage file
    init         Initialize a manage shell in current...
    shell        Runs a Python shell with context

And you can even customize namespace for each module separately
---------------------------------------------------------------

.. note:: If **namespaced** is true all commands will be namespaced, set it to false in order to define separately


.. code-block:: yaml

  click_commands:
    - module: commands.system
      namespace: sys
    - module: commands.user
      namespace: user

Now you run **manage --help** and you can see all the commands in the same module will be namespaced.

.. code-block:: console

  $ manage --help
  ...
  Commands:
    user_create_user  Create a new user
    sys_clear_cache  Clear the system cache
    debug        Shows the parsed manage file
    init         Initialize a manage shell in current...
    shell        Runs a Python shell with context


2. Defining your inline commands in manage file directly
--------------------------------------------------------

Sometimes your command is so simple that you do not want (or can't) have a custom module,
so you can put all your commands in yaml file directly.

.. code-block:: yaml

    inline_commands:
      - name: clear_cache
        help_text: Executes inline code to clear the cache
        context:
          - sys
          - pprint
        options:
          --days:
            default: 100
        code: |
          pprint.pprint({'clean_days': days, 'path': sys.path})


Now running **manage --help**

.. code-block:: console

  $ manage --help
  ...
  Commands:
    clear_cache  Executes inline code to clear the cache
    debug        Shows the parsed manage file
    init         Initialize a manage shell in current...
    shell        Runs a Python shell with context


And you can run using

.. code-block:: console

  $ manage clear_cache --days 15

3. Using general functions as commands
--------------------------------------
And if you already has some defined function (any callable works).

.. code-block:: python

    # my_system.functions.py
    def create_user(name, password):
        print("Creating user %s" % name)



.. code-block:: yaml

    function_commands:
      - function: my_system.functions.create_user
        name: new_user
        help_text: Create new user
        options:
          --name:
            required: true
          --password:
            required: true


Now running **manage --help**

.. code-block:: console

  $ manage --help
  ...
  Commands:
    new_user     Create new user
    debug        Shows the parsed manage file
    init         Initialize a manage shell in current...
    shell        Runs a Python shell with context

  $ manage new_user --name=Bruno --password=1234
  Creating user Bruno


Further Explanations
====================

- You can say, **how this is useful?**, There's no need to get a separate package and configure everything in yaml, just use iPython to do it. Besides, IPython configuration has a lot more options and capabilities.
- So I say: Nice! **If you don't like it, dont't use it!**

Credits
=======

- This is inspired by **Django's manage.py command**
- This is based on click_
- This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _click: http://click.pocoo.org
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
