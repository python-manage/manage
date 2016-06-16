# coding: utf-8

import click


@click.command()
@click.option('--name')
@click.option('--passwd')
def create_user(name, passwd):
    """Create a new user"""
    click.echo('Creating the user %s' % name)


@click.command()
@click.option('--name')
def create_group(name):
    """Create a new group"""
    click.echo('Creating the group %s' % name)


def this_is_not_command(foo, bar):
    """Will not be added"""
    pass
