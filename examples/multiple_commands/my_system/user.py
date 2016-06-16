# coding: utf-8

import click


@click.command()
@click.option('--name')
@click.option('--passwd')
def create_user(name, passwd):
    """Create a new user"""
    click.echo('Creating the user %s' % name)


def this_is_not_command(foo, bar):
    """Will not be added"""
    pass
