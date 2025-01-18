
import click
from . import build_something

@click.command()
@click.argument('input_file')
def main(input_file):
    """Build outputs from the input markdown file."""
    build_something.process(input_file)

if __name__ == '__main__':
    main()