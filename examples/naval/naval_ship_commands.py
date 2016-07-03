import click


@click.command('shoot')
@click.argument('ship')
@click.argument('x', type=float)
@click.argument('y', type=float)
def ship_shoot(ship, x, y):
    """Makes SHIP fire to X,Y."""
    click.echo('Ship %s fires to %s,%s' % (ship, x, y))
