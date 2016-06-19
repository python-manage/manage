default_manage_dict = {
    'project_name': 'Project',
    'help_text': "This is the {project_name} interactive shell",
    'shell': {  # Preferences for 'manage shell'
        'banner': {  # Banner is the message printed on top of console
            'enabled': True,  # It can be disabled
            # Here it goes the message
            'message': "Manage Interactive Shell! edit your `manage.yml`",
        },
        'auto_import': {  # Objects to be auto imported to shell context
            'display': True,  # Weather to print all a list of all objects
            'objects': {}
        },
        'readline_enabled': True,
        'init_script': 'print("Starting interactive shell!")'
    },
    'function_commands': [],
    'click_commands': [],
    'inline_commands': [],
}
