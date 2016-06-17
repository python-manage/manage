import sys
import os
import click
import pkgutil
import importlib

from inspect import getmembers
from click.core import BaseCommand
from manage.utils import import_string


def add_click_commands(module, cli, command_dict, namespaced):
    """Loads all click commands"""
    module_commands = [
        item for item in getmembers(module)
        if isinstance(item[1], BaseCommand)
    ]
    options = command_dict.get('config', {})
    namespace = command_dict.get('namespace')
    for name, function in module_commands:
        f_options = options.get(name, {})
        command_name = f_options.get('name', name)
        if namespace:
            command_name = '{}_{}'.format(namespace, command_name)
        elif namespaced:
            module_namespace = module.__name__.split('.')[-1]
            command_name = '{}_{}'.format(module_namespace, command_name)
        function.short_help = f_options.get('help_text', function.short_help)
        cli.add_command(function, name=command_name)


def make_command_from_string(code, cmd_context, options, help_text=None):
    def _command(**kwargs):
        exec (code, cmd_context, kwargs)

    if help_text:
        _command.__doc__ = help_text
    _command = click.command()(_command)
    for name, option in options.items():
        _command = click.option(name, **option)(_command)
    return _command


def get_context(context):
    return {item: import_string(item) for item in context}


def load_commands(cli, manage_dict):
    """Loads the commands defined in manage file"""
    namespaced = manage_dict.get('namespaced')

    # get click commands
    commands = manage_dict.get('click_commands', [])
    for command_dict in commands:
        root_module = import_string(command_dict['module'])
        if getattr(root_module, '__path__', None):
            # This is a package
            iter_modules = pkgutil.iter_modules(
                root_module.__path__, prefix=root_module.__name__ + '.'
            )
            submodules_names = [item[1] for item in iter_modules]
            submodules = [import_string(name) for name in submodules_names]
            for module in submodules:
                add_click_commands(module, cli, command_dict, namespaced)
        else:
            # a single file module
            add_click_commands(root_module, cli, command_dict, namespaced)

    # get inline commands
    commands = manage_dict.get('inline_commands', [])
    for command_dict in commands:
        name = command_dict['name']
        help_text = command_dict.get('help_text')
        options = command_dict.get('options', {})
        context = command_dict.get('context', [])
        code = command_dict['code']
        cli.add_command(
            make_command_from_string(
                code=code,
                cmd_context=get_context(context),
                options=options,
                help_text=help_text
            ),
            name=name
        )


class CommandsCollector(click.MultiCommand):
    """A MultiCommand to collect all click commands from a given
    modules path and base name for the module.
    The commands functions needs to be in a module inside commands
    folder and the name of the file will be used as the command name.
    """

    def __init__(self, modules_path, base_module_name, **attrs):
        click.MultiCommand.__init__(self, **attrs)
        self.base_module_name = base_module_name
        self.modules_path = modules_path

    def list_commands(self, *args, **kwargs):
        commands = []
        for _path, _dir, _ in os.walk(self.modules_path):
            if 'commands' not in _dir:
                continue
            for filename in os.listdir(os.path.join(_path, 'commands')):
                if filename.endswith('.py') and filename != '__init__.py':
                    cmd = filename[:-3]
                    _, module_name = os.path.split(_path)
                    commands.append('{0}_{1}'.format(module_name, cmd))
        commands.sort()
        return commands

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            splitted = name.split('_')
            if len(splitted) <= 1:
                return
            module_name, command_name = splitted
            if not all([module_name, command_name]):
                return
            module = '{0}.{1}.commands.{2}'.format(
                self.base_module_name,
                module_name,
                command_name)
            mod = importlib.import_module(module)
        except ImportError:
            return
        return getattr(mod, 'cli', None)
