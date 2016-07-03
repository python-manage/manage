import click
import pkgutil
import import_string
from six import exec_
from six.moves import builtins
from inspect import getmembers
from click.core import BaseCommand


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
        command_name = f_options.get('name', getattr(function, 'name', name))
        if namespace:
            command_name = '{}_{}'.format(namespace, command_name)
        elif namespaced:
            module_namespace = module.__name__.split('.')[-1]
            command_name = '{}_{}'.format(module_namespace, command_name)
        function.short_help = f_options.get('help_text', function.short_help)
        cli.add_command(function, name=command_name)


def handle_option_and_arg_data(data):
    data = data or {}
    if 'type' in data:
        data['type'] = getattr(builtins, data['type'])
    if 'help_text' in data:
        data['help'] = data.pop('help_text')
    return data


def handle_options_and_args(_command, arguments, options):

    for argument in arguments:
        if isinstance(argument, dict):
            _command = click.argument(
                list(argument.keys())[0],
                **handle_option_and_arg_data(list(argument.values())[0])
            )(_command)
        else:
            _command = click.argument(argument)(_command)

    if isinstance(options, dict):
        for name, data in options.items():
            data = handle_option_and_arg_data(data)
            _command = click.option(name, **data)(_command)
    else:
        for name in options:
            _command = click.option(name)(_command)
    return _command


def make_command_from_function(function, options,
                               help_text=None, arguments=None):

    if help_text:
        function.__doc__ = help_text

    function = click.command()(function)
    function = handle_options_and_args(function, arguments, options)
    return function


def make_command_from_string(code, cmd_context, options,
                             help_text=None, arguments=None):
    def _command(*args, **kwargs):
        exec_(code, cmd_context, kwargs)

    return make_command_from_function(_command, options, help_text, arguments)


def get_context(context):
    return {item: import_string(item) for item in context}


def load_commands(cli, manage_dict):
    """Loads the commands defined in manage file"""
    namespaced = manage_dict.get('namespaced')

    # get click commands
    commands = manage_dict.get('click_commands', [])
    for command_dict in commands:
        root_module = import_string(command_dict['module'])
        group = cli.manage_groups.get(command_dict.get('group'), cli)
        if getattr(root_module, '__path__', None):
            # This is a package
            iter_modules = pkgutil.iter_modules(
                root_module.__path__, prefix=root_module.__name__ + '.'
            )
            submodules_names = [item[1] for item in iter_modules]
            submodules = [import_string(name) for name in submodules_names]
            for module in submodules:
                add_click_commands(module, group, command_dict, namespaced)
        else:
            # a single file module
            add_click_commands(root_module, group, command_dict, namespaced)

    # get inline commands
    commands = manage_dict.get('inline_commands', [])
    for command_dict in commands:
        name = command_dict['name']
        help_text = command_dict.get('help_text')
        options = command_dict.get('options', {})
        arguments = command_dict.get('arguments', {})
        context = command_dict.get('context', [])
        code = command_dict['code']
        group = cli.manage_groups.get(command_dict.get('group'), cli)
        group.add_command(
            make_command_from_string(
                code=code,
                cmd_context=get_context(context),
                options=options,
                arguments=arguments,
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
        arguments = command_dict.get('arguments', {})
        function = import_string(command_dict['function'])
        group = cli.manage_groups.get(command_dict.get('group'), cli)
        group.add_command(
            make_command_from_function(
                function=function,
                options=options,
                arguments=arguments,
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


def load_groups(cli, manage_dict):
    cli.manage_groups = {}
    groups = manage_dict.get('groups')
    if not groups:
        return
    is_dict = isinstance(groups[0], dict)
    for group in groups:
        if is_dict:
            for group_name, data in group.items():
                data = data or {}
                if 'help_text' in data:
                    data['help'] = data.pop('help_text')
                cli.manage_groups[group_name] = cli.group(
                    name=group_name, **data
                )(lambda: None)
        else:
            cli.manage_groups[group] = cli.group(name=group)(lambda: None)
