#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_manage
----------------------------------

Tests for `manage` module.
py.test should run with --boxed argument
"""
import os
from click.testing import CliRunner
from manage.cli import cli, init_cli

BASEPATH = os.path.abspath('.')


class TestManage(object):

    @classmethod
    def setup_class(cls):
        pass

    def go_to_example(self, path):
        path = os.path.join(BASEPATH, 'examples', path)
        os.chdir(path)
        init_cli(cli, reset=True)

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'shell' in result.output
        help_result = runner.invoke(cli, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

    def test_custom_command_names(self):
        runner = CliRunner()
        self.go_to_example('custom_command_names')
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'new_user' in result.output
        assert 'new_group' in result.output
        create_user = runner.invoke(
            cli, ['new_user', '--name=Bruno'])
        assert 'Creating the user Bruno' in create_user.output
        create_group = runner.invoke(
            cli, ['new_group', '--name=Users'])
        assert 'Creating the group Users' in create_group.output

    def test_custom_namespaces(self):
        runner = CliRunner()
        self.go_to_example('custom_namespaces')
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'bar_create_user' in result.output
        assert 'foo_new_group' in result.output
        create_user = runner.invoke(
            cli, ['bar_create_user', '--name=Bruno'])
        assert 'Creating the user Bruno' in create_user.output
        create_group = runner.invoke(
            cli, ['foo_new_group', '--name=Users'])
        assert 'Creating the group Users' in create_group.output

    def test_function_commands(self):
        runner = CliRunner()
        self.go_to_example('function_commands')
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'new_user' in result.output
        assert 'Error: Missing option "--password"' in runner.invoke(
            cli, ['new_user', '--name=Bruno']
        ).output
        create_user = runner.invoke(
            cli, ['new_user', '--name=Bruno', '--password=123'])
        assert 'Creating user Bruno' in create_user.output

    def test_inline_commands(self):
        runner = CliRunner()
        self.go_to_example('inline_commands')
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'clear_cache' in result.output
        clear_cache = runner.invoke(
            cli, ['clear_cache'])
        assert "'clean_days': 100" in clear_cache.output

        clear_cache = runner.invoke(
            cli, ['clear_cache', '--days=15'])
        assert "'clean_days': 15" in clear_cache.output

    def test_multiple_click_commands(self):
        runner = CliRunner()
        self.go_to_example('multiple_commands')
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'create_user' in result.output
        assert 'create_group' in result.output
        create_user = runner.invoke(
            cli, ['create_user', '--name=Bruno'])
        assert 'Creating the user Bruno' in create_user.output
        create_group = runner.invoke(
            cli, ['create_group', '--name=Users'])
        assert 'Creating the group Users' in create_group.output

    def test_namespaced_commands(self):
        runner = CliRunner()
        self.go_to_example('namespaced_commands')
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'user_create_user' in result.output
        assert 'group_new_group' in result.output
        create_user = runner.invoke(
            cli, ['user_create_user', '--name=Bruno'])
        assert 'Creating the user Bruno' in create_user.output
        create_group = runner.invoke(
            cli, ['group_new_group', '--name=Users'])
        assert 'Creating the group Users' in create_group.output

    def test_simple(self):
        runner = CliRunner()
        self.go_to_example('simple')
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0

    def test_simple_commands(self):
        runner = CliRunner()
        self.go_to_example('simple_commands')
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'create_user' in result.output
        assert 'create_group' in result.output
        create_user = runner.invoke(
            cli, ['create_user', '--name=Bruno'])
        assert 'Creating the user Bruno' in create_user.output
        create_group = runner.invoke(
            cli, ['create_group', '--name=Users'])
        assert 'Creating the group Users' in create_group.output

    def test_naval(self):
        runner = CliRunner()
        self.go_to_example('naval')

        # ship and mine is there?
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'ship' in result.output
        assert 'mine' in result.output

        # help for ship
        result = runner.invoke(cli, ['ship', '--help'])
        assert result.exit_code == 0
        assert 'new' in result.output
        assert 'move' in result.output
        assert 'shoot' in result.output

        # help for mine
        result = runner.invoke(cli, ['mine', '--help'])
        assert result.exit_code == 0
        assert 'set' in result.output
        assert 'remove' in result.output

        # ship new
        result = runner.invoke(cli, ['ship', 'new', 'FireStorm'])
        assert result.exit_code == 0
        assert result.output == 'Created ship FireStorm\n'

        # ship move
        result = runner.invoke(
            cli, ['ship', 'move', 'FireStorm', '12', '34', '--speed', '90']
        )
        assert result.exit_code == 0
        assert result.output == (
            'Moving ship FireStorm to 12.0,34.0 with speed 90\n'
        )

        # ship shoot
        result = runner.invoke(cli, ['ship', 'shoot', 'FireStorm', '30', '45'])
        assert result.exit_code == 0
        assert result.output == 'Ship FireStorm fires to 30.0,45.0\n'

        # mine set
        result = runner.invoke(cli, ['mine', 'set', '10', '20'])
        assert result.exit_code == 0
        assert result.output == 'Set moored mine at 10.0,20.0\n'

        result = runner.invoke(cli, ['mine', 'set', '10', '20', '--drifting'])
        assert result.exit_code == 0
        assert result.output == 'Set drifting mine at 10.0,20.0\n'

        # mine remove
        result = runner.invoke(cli, ['mine', 'remove', '10', '20'])
        assert result.exit_code == 0
        assert result.output == 'Removed mine at 10.0,20.0\n'

    @classmethod
    def teardown_class(cls):
        pass
