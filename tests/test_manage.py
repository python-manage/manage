#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_manage
----------------------------------

Tests for `manage` module.
"""

# import pytest

# from contextlib import contextmanager
from click.testing import CliRunner

from manage.cli import cli


class TestManage(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'shell' in result.output
        help_result = runner.invoke(cli, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

    @classmethod
    def teardown_class(cls):
        pass
