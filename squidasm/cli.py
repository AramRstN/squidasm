import click
import squidasm
from squidasm.run import simulate_apps

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Command line interface for managing virtual python environments."""
    pass


###########
# version #
###########

@cli.command()
def version():
    """
    Prints the version of squidasm.
    """
    print(squidasm.__version__)


###########
# execute #
###########

@cli.command()
@click.option("--app-dir", type=str, default=None,
              help="Path to app directory. "
                   "Defaults to CWD."
              )
@click.option("--track-lines/--no-track-lines", default=True)
@click.option("--network-config-file", type=str, default=None,
              help="Explicitly choose the network config file, "
                   "default is `app-folder/network.yaml`."
              )
@click.option("--app-config-dir", type=str, default=None,
              help="Explicitly choose the app config directory, "
                   "default is `app-folder`."
              )
@click.option("--log-dir", type=str, default=None,
              help="Explicitly choose the log directory, "
                   "default is `app-folder/log`."
              )
@click.option("--log-level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]), default="WARNING",
              help="What log-level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL)."
                   "Note, this affects logging to stderr, not logging instructions to file."
              )
def simulate(app_dir, track_lines, network_config_file, app_config_dir, log_dir, log_level):
    """
    Executes a given NetQASM file using a specified executioner.
    """
    simulate_apps(
        app_dir=app_dir,
        track_lines=track_lines,
        network_config_file=network_config_file,
        app_config_dir=app_config_dir,
        log_dir=log_dir,
        log_level=log_level,
    )


if __name__ == '__main__':
    cli()