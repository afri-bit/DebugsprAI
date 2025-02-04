import click

import debugspray.core as core


@click.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.argument("issue_file", type=click.Path(exists=True))
@click.option("--result-folder", "-rf", type=click.Path(), default="results")
def debugspray(project_path, issue_file, result_folder):
    core.debug_issue(project_path, issue_file, result_folder)


def run():
    debugspray()
