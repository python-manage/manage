#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import code
import yaml
import click
import readline
import importlib
import rlcompleter
from .template import default_manage_dict


MANAGE_FILE = 'manage.yml'

if os.path.exists(MANAGE_FILE):
    with open(MANAGE_FILE) as manage_file:
        manage_dict = yaml.load(manage_file)
else:
    manage_dict = default_manage_dict


@click.group()
def core_cmd():
    """ Core commands wrapper """
    pass


class DynamicImporter(object):
    def __init__(self, module_name):
        self.module_name = module_name

    def __getattr__(self, item):
        return importlib.import_module(
            '{0}.{1}'.format(self.module_name, item))


@core_cmd.command()
@click.option('--banner')
def init(banner):
    """Initialize a manage shell in current directory
        $ manage init --banner="My awesome app shell"
        initializing manage...
        creating manage.yml
    """
    if os.path.exists(MANAGE_FILE):
        if not click.confirm('Do you want to rewrite manage.yml?'):
            return
        else:
            "Copy the file"

    with open(MANAGE_FILE, 'w') as manage_file:
        data = default_manage_dict
        data['shell']['banner']['message'] = banner
        manage_file.write(yaml.dump(data, default_flow_style=False))


@core_cmd.command()
@click.option('--ipython/--no-ipython', default=True)
def shell(ipython):
    """Runs a Python shell with context"""
    _vars = globals()
    _vars.update(locals())
    auto_imported = {
    }
    _vars.update(auto_imported)
    banner_msg = (
        '{banner_message}\n'
        '\tAuto imported: {auto_imported}\n'
    ).format(
        auto_imported=auto_imported.keys(),
        banner_message=manage_dict['shell']['banner']['message']
    )
    readline.set_completer(rlcompleter.Completer(_vars).complete)
    readline.parse_and_bind('tab: complete')
    try:
        if ipython is True:
            from IPython import start_ipython
            from traitlets.config import Config
            c = Config()
            c.TerminalInteractiveShell.banner2 = banner_msg
            start_ipython(argv=[], user_ns=_vars, config=c)
        else:
            raise ImportError
    except ImportError:
        shell = code.InteractiveConsole(_vars)
        shell.interact(banner=banner_msg)


help_text = """
    PROGRAM Interactive shell!
    """
main = click.CommandCollection(help=help_text)
main.add_source(core_cmd)

if __name__ == '__main__':
    main()
