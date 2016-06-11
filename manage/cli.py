#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import code
import readline
import rlcompleter
# import importlib


@click.group()
def core_cmd():
    """ Core commands wrapper """
    pass


# class RobotteloLoader(object):
#     def __getattr__(self, item):
#         return importlib.import_module('robottelo.{0}'.format(item))


@core_cmd.command()
@click.option('--ipython/--no-ipython', default=True)
def shell(ipython):
    """Runs a Python shell with Robottelo context"""
    _vars = globals()
    _vars.update(locals())
    auto_imported = {
    }
    _vars.update(auto_imported)
    banner_msg = (
        'Welcome to PROGRAM interactive shell\n'
        '\tAuto imported: {0}\n'
    ).format(auto_imported.keys())
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
