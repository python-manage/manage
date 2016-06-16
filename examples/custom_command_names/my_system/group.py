# coding: utf-8

import click


@click.command()
@click.option('--name')
def create_group(name):
    """Create a new group"""
    click.echo('Creating the group %s' % name)


def this_is_not_command(foo, bar):
    """Will not be added"""
    pass
