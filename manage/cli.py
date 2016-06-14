#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import code
import json
import yaml
import click
import readline
import rlcompleter
from manage.template import default_manage_dict
from manage.auto_import import import_objects, exec_init, exec_init_script

MANAGE_FILE = 'manage.yml'
HIDDEN_MANAGE_FILE = '.{0}'.format(MANAGE_FILE)


def load_manage_dict():
    if os.path.exists(MANAGE_FILE):
        manage_filename = MANAGE_FILE
    elif os.path.exists(HIDDEN_MANAGE_FILE):
        manage_filename = HIDDEN_MANAGE_FILE
    else:
        return default_manage_dict
    with open(manage_filename) as manage_file:
        return yaml.load(manage_file)


manage_dict = load_manage_dict()


@click.group()
def core_cmd():
    """ Core commands wrapper """
    pass


@core_cmd.command()
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
        data['shell']['banner']['message'] = banner
        output.write(yaml.dump(data, default_flow_style=False))


@core_cmd.command()
def debug():
    """Shows the parsed manage file"""
    print(json.dumps(manage_dict, indent=2))


@core_cmd.command()
@click.option('--ipython/--no-ipython', default=True)
def shell(ipython):
    """Runs a Python shell with context"""
    _vars = globals()
    _vars.update(locals())
    auto_imported = import_objects(manage_dict)
    _vars.update(auto_imported)
    msgs = []
    if manage_dict['shell']['banner']['enabled']:
        msgs.append(
            manage_dict['shell']['banner']['message'].format(**manage_dict)
        )
    if manage_dict['shell']['auto_import']['display']:
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


main = click.CommandCollection(
    help=manage_dict.get(
        'help_text', '{project_name} Interactive shell!'
    ).format(**manage_dict)
)

main.add_source(core_cmd)

if __name__ == '__main__':
    main()
