import click
import pkgutil
from six import exec_
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
        exec_(code, cmd_context, kwargs)

    if help_text:
        _command.__doc__ = help_text
    _command = click.command()(_command)
    for name, option in options.items():
        _command = click.option(name, **option)(_command)
    return _command


def make_command_from_function(function, options, help_text=None):

    if help_text:
        function.__doc__ = help_text

    function = click.command()(function)
    for name, option in options.items():
        function = click.option(name, **option)(function)
    return function


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

    # get function commands
    commands = manage_dict.get('function_commands', [])
    for command_dict in commands:
        name = command_dict['name']
        help_text = command_dict.get('help_text')
        options = command_dict.get('options', {})
        function = import_string(command_dict['function'])
        cli.add_command(
            make_command_from_function(
                function=function,
                options=options,
                help_text=help_text
            ),
            name=name
        )


def load_command_sources(manager, manage_dict):
    manage_sources = manage_dict.get('command_sources', [])
    for source_data in manage_sources:
        if isinstance(source_data, dict):
            source = import_string(source_data['name'])
            manager.add_source(
                source(
                    *source_data.get('args', []),
                    **source_data.get('kwargs', {})
                )
                if callable(source)
                else source
            )
        else:
            source = import_string(source_data)
            manager.add_source(source() if callable(source) else source)
