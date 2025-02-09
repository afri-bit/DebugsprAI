import click
import json

import debugsprai.core as core
from debugsprai.parser import parse_markdown_issue
from debugsprai.models import Issue


@click.group()
def debugsprai():
    pass


@debugsprai.command()
@click.argument("markdown_file", type=click.Path(exists=True))
@click.option(
    "--output", "-o", type=click.Path(), default="output.json", required=False
)
def parse(markdown_file, output):
    """
    Sub command to parse issue markdown file to json format

    Args:
        markdown_file (click.Path): input markdown file path
        output (str): output file path and name
    """
    issue: Issue | None = None

    with open(markdown_file, "r") as f:
        markdown = f.read()
        issue = parse_markdown_issue(markdown)

    if issue:
        with open(output, "w") as f:
            f.write(issue.model_dump_json(indent=2))
    else:
        raise ValueError("Failed on parsing the issue.")


@debugsprai.command()
@click.argument("issue_file", type=click.Path(exists=True))
@click.option("--result-folder", "-rf", type=click.Path(), default=".airesults", required=False)
def debug(issue_file, result_folder):
    """_summary_

    Args:
        project_path (_type_): _description_
        issue_file (bool): _description_
        result_folder (_type_): _description_
    """

    issue: Issue | None = None

    with open(issue_file, "r") as file:
        data = json.load(file)
        issue = Issue.model_validate(data)

    core.debug_issue(issue=issue, result_folder=result_folder)


def run():
    debugsprai()
