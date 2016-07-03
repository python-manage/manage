#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import copy
import code
import json
import yaml
import click
import readline
import rlcompleter
from manage import __version__
from manage.template import default_manage_dict
from manage.auto_import import import_objects, exec_init, exec_init_script
from manage.commands_collector import (
    load_commands, load_command_sources, load_groups
)

MANAGE_FILE = 'manage.yml'
HIDDEN_MANAGE_FILE = '.{0}'.format(MANAGE_FILE)
MANAGE_DICT = {}


def load_manage_dict(filename=None):
    manage_filename = None
    if not MANAGE_DICT:
        if filename:
            manage_filename = filename
        elif os.path.exists(MANAGE_FILE):
            manage_filename = MANAGE_FILE
        elif os.path.exists(HIDDEN_MANAGE_FILE):
            manage_filename = HIDDEN_MANAGE_FILE
        else:
            MANAGE_DICT.update(copy.deepcopy(default_manage_dict))
            MANAGE_DICT['shell']['banner']['message'] = (
                "WARNING: This is not a managed project\n"
                "\tPlease `exit()` and \n"
                "\trun `$ manage init`\n"
                "\tand edit `manage.yml` file with desired options"
            )
            MANAGE_DICT['shell']['auto_import']['display'] = False
        if manage_filename:
            with open(manage_filename) as manage_file:
                MANAGE_DICT.update(yaml.load(manage_file))
    return MANAGE_DICT


class Config(object):

    def __init__(self):
        self.filename = None
        self._manage_dict = None

    @property
    def manage_dict(self):
        if not self._manage_dict:
            self._manage_dict = load_manage_dict(self.filename)
        return self._manage_dict


@click.group(no_args_is_help=False)
def cli():
    """ Core commands wrapper """


@cli.command()
@click.option('--banner')
@click.option('--hidden/--no-hidden', default=False)
@click.option('--backup/--no-backup', default=True)
def init(banner, hidden, backup):
    """Initialize a manage shell in current directory
        $ manage init --banner="My awesome app shell"
        initializing manage...
        creating manage.yml
    """
    manage_file = HIDDEN_MANAGE_FILE if hidden else MANAGE_FILE
    if os.path.exists(manage_file):
        if not click.confirm('Rewrite {0}?'.format(manage_file)):
            return

        if backup:
            bck = '.bck_{0}'.format(manage_file)
            with open(manage_file, 'r') as source, open(bck, 'w') as bck_file:
                bck_file.write(source.read())

    with open(manage_file, 'w') as output:
        data = default_manage_dict
        if banner:
            data['shell']['banner']['message'] = banner
        output.write(yaml.dump(data, default_flow_style=False))


@cli.command()
@click.option('--version', '-V', is_flag=True, default=False)
def debug(version=False):
    """Shows the parsed manage file -V shows version"""
    if version:
        print(__version__)
        return
    print(json.dumps(MANAGE_DICT, indent=2))


def create_shell(console, manage_dict=None, extra_vars=None):
    """Creates the shell"""
    manage_dict = manage_dict or MANAGE_DICT
    _vars = globals()
    _vars.update(locals())
    auto_imported = import_objects(manage_dict)
    if extra_vars:
        auto_imported.update(extra_vars)
    _vars.update(auto_imported)
    msgs = []
    if manage_dict['shell']['banner']['enabled']:
        msgs.append(
            manage_dict['shell']['banner']['message'].format(**manage_dict)
        )
    if auto_imported and manage_dict['shell']['auto_import']['display']:
        auto_imported_names = [
            key for key in auto_imported.keys()
            if key not in ['__builtins__', 'builtins']
        ]
        msgs.append('\tAuto imported: {0}\n'.format(auto_imported_names))

    banner_msg = u'\n'.join(msgs)

    if manage_dict['shell']['readline_enabled']:
        readline.set_completer(rlcompleter.Completer(_vars).complete)
        readline.parse_and_bind('tab: complete')

    exec_init(manage_dict, _vars)
    exec_init_script(manage_dict, _vars)

    if console == 'ptpython':
        try:
            from ptpython.repl import embed
            embed({}, _vars)
        except ImportError:
            click.echo("ptpython is not installed!")
        return

    if console == 'bpython':
        try:
            from bpython import embed
            embed(locals_=_vars, banner=banner_msg)
        except ImportError:
            click.echo("bpython is not installed!")
        return

    try:
        if console == 'ipython':
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


@cli.command()
@click.option('console', '--ipython', default=True, flag_value='ipython',
              help='Start with ipython console')
@click.option('console', '--ptpython', flag_value='ptpython',
              help='Start with ptpython console')
@click.option('console', '--bpython', flag_value='bpython',
              help='Start with bpython console')
@click.option('console', '--python', flag_value='python',
              help='Start with python console')
def shell(console):
    """Runs a Python shell with context"""
    return create_shell(
        MANAGE_DICT.get('shell', {}).get('console', console),
        MANAGE_DICT
    )


def load_manage_dict_from_sys_args():
    single_option = [item for item in sys.argv if '--managefile=' in item]
    if single_option:
        filename = single_option[0].split('=')[-1]
        sys.argv.remove(single_option[0])
    elif '--managefile' in sys.argv:
        filename = sys.argv[sys.argv.index('--managefile') + 1]
        sys.argv.remove('--managefile')
        sys.argv.remove(filename)
    else:
        filename = None
    load_manage_dict(filename)


def init_cli(cli_obj, reset=False):
    if reset:
        global MANAGE_DICT
        MANAGE_DICT = {}
    sys.path.insert(0, '.')
    load_manage_dict_from_sys_args()
    cli.help = MANAGE_DICT.get(
        'help_text', '{project_name} Interactive shell!'
    ).format(**MANAGE_DICT)
    load_groups(cli, MANAGE_DICT)
    load_commands(cli, MANAGE_DICT)
    manager = click.CommandCollection(help=cli.help, no_args_is_help=False)
    manager.add_source(cli)
    load_command_sources(manager, MANAGE_DICT)
    for item in MANAGE_DICT.get('disabled', []):
        cli.commands.pop(item, None)
    return manager


def main():
    manager = init_cli(cli)
    return manager()


if __name__ == '__main__':
    main()
