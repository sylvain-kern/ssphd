import click
from ssphd.build import build

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('config_file', type=click.Path())
def main(input_file, config_file):
    """Build outputs from the input markdown file."""
    build(input_file, config_file)

if __name__ == '__main__':
    main()