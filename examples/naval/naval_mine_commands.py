import click


@click.command('set')
@click.argument('x', type=float)
@click.argument('y', type=float)
@click.option('ty', '--moored', flag_value='moored',
              default=True,
              help='Moored (anchored) mine. Default.')
@click.option('ty', '--drifting', flag_value='drifting',
              help='Drifting mine.')
def mine_set(x, y, ty):
    """Sets a mine at a specific coordinate."""
    click.echo('Set %s mine at %s,%s' % (ty, x, y))
