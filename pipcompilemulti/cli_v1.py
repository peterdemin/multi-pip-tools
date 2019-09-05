"""First version of command line interface"""

import logging

import click

from .options import OPTIONS
from .actions import recompile
from .verify import verify_environments
from .features import FEATURES


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--compatible', '-c', multiple=True,
              help='Glob expression for packages with compatible (~=) '
                   'version constraint. Can be supplied multiple times.')
@click.option('--forbid-post', '-p', multiple=True,
              help="Environment name (base, test, etc) that cannot have "
                   'packages with post-release versions (1.2.3.post777). '
                   'Can be supplied multiple times.')
@click.option('--generate-hashes', '-g', multiple=True,
              help='Environment name (base, test, etc) that needs '
                   'packages hashes. '
                   'Can be supplied multiple times.')
@click.option('--directory', '-d', default=OPTIONS['base_dir'],
              help='Directory path with requirements files.')
@click.option('--header', '-h', default='',
              help='File path with custom header text for generated files.')
@click.option('--only-name', '-n', multiple=True,
              help='Compile only for passed environment names and their '
                   'references. Can be supplied multiple times.')
@click.option('--upgrade/--no-upgrade', default=True,
              help='Upgrade package version (default true)')
@click.option('--upgrade-package', '-P', multiple=True,
              help='Only upgrade named package. Can be supplied multiple times.')
@FEATURES.bind
def cli(ctx, compatible, forbid_post, generate_hashes, directory,
        header, only_name, upgrade, upgrade_package):
    """Recompile"""

    if upgrade_package:
        # pip-compile only accepts one of --upgrade or --upgrade-package
        upgrade = False

    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    OPTIONS.update({
        'compatible_patterns': compatible,
        'forbid_post': set(forbid_post),
        'add_hashes': set(generate_hashes),
        'base_dir': directory,
        'header_file': header or None,
        'include_names': only_name,
        'upgrade': upgrade,
        'upgrade_packages': upgrade_package,
    })
    if ctx.invoked_subcommand is None:
        recompile()


@cli.command()
@click.pass_context
def verify(ctx):
    """
    For each environment verify hash comments and report failures.
    If any failure occured, exit with code 1.
    """
    ctx.exit(0
             if verify_environments()
             else 1)
