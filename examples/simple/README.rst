This is the SIMPLE example, it is just a folder with a :code:`manage.yml`

.. code-block:: yaml

  project_name: My Simple Project
  help_text: |
    This is the {project_name} interactive shell
    You can have commands or open the shell
  shell:
    readline_enabled: true
    banner:
      enabled: true
      message: 'Hello {project_name} World'
    auto_import:
      display: true
      objects:
        manage.utils.import_string:
        os.path:
          as: path
          init:
            exists:
              kwargs:
                path: /tmp
          init_script: |
            print("path object is:")
            print(type(path))
            print("Hello path from init_script")
        sys.path:
          as: sp
          init:
            insert:
              args:
                - 0
                - /tmp/add_on_object_init
          init_script: |
            def function():
                assert isinstance(sp, list)
                return type(sp)
            print(function())
    init:
      sys.path.append:
        args:
          - /tmp/added_on_shell_init
    init_script: |
      # add a path to sys.path
      import sys
      sys.path.append('/tmp/added_on_shell_init_script')
      assert '/tmp/added_on_shell_init' in sys.path
      assert '/tmp/add_on_object_init' in sys.path
      assert '/tmp/added_on_shell_init_script' in sys.path


and it can be used as:

.. code-block:: console

  $ pip install manage

.. code-block:: console

  $ cd examples/simple/
  $ manage
  Usage: manage [OPTIONS] COMMAND [ARGS]...

  This is the My Simple Project interactive shell You can have commands or
  open the shell

  Options:
    --help  Show this message and exit.

  Commands:
    debug  Shows the parsed manage file
    init   Initialize a manage shell in current...
    shell  Runs a Python shell with context


And the shell acording to defined attributes in **manage.yml**:

.. code-block:: console

  $ manage shell
  <type 'list'>
  path object is:
  <type 'module'>
  Hello path from init_script
  Python 2.7.11 (default, Mar 31 2016, 20:46:51)
  IPython 4.2.0 -- An enhanced Interactive Python.
  ...

  Hello My Simple Project World
	   Auto imported: ['import_string', 'path', 'function', 'sp']

  In [1]: 
