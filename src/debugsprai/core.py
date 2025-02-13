import os
import json
import pathlib
from string import Template

import google.generativeai as genai

import debugsprai.logger as logger
import debugsprai.prompt as prompt
from debugsprai.models import Issue

logger = logger.setup_logger(__name__)


programming_languages = {
    "python": "py",
}


def debug_issue(issue: Issue, result_folder: str = ".airesults"):
    """
    The core functionality of debugsprai.
    This function will read the issue object go through the project files that may
    be relevant to the issue and will send prompting text to the Gemini API to
    generate fix suggestions for the bugs reported.

    Args:
        project_path (str): _description_
        issue_file_path (str): _description_
        result_folder (str, optional): _description_. Defaults to "results".

    Raises:
        ValueError: _description_
    """

    # Setup the pathing based on the issue object
    project_path = pathlib.Path(issue.project_folder).absolute().resolve()

    # Configuration the project path
    if not os.path.exists(project_path):
        logger.error(f"Project path does not exist: '{project_path}'")
        return

        # Get the additional path from the issue file
    src_folder = project_path.joinpath(issue.source_folder).resolve()
    test_folder = project_path.joinpath(issue.test_folder).resolve()
    result_folder = pathlib.Path(result_folder).absolute().resolve()
    project_result_folder = result_folder.joinpath("project").resolve()
    json_mapping_file = result_folder.joinpath("file_mapping.json").resolve()

    if issue.programming_language.lower() not in programming_languages.keys():
        raise ValueError(
            f"Programming language '{issue.programming_language}' not supported."
        )
    
    # Get the file extension
    file_extension = programming_languages[issue.programming_language.lower()]

    # ========== Google Gemini Configuration ==========
    # Configure API Key
    GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME") or "gemini-2.0-flash-exp"
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("Please set the 'GEMINI_API_KEY' environment variable")

    # Configuration of the generative model
    genai.configure(api_key=GEMINI_API_KEY)

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL_NAME,
        generation_config=generation_config,
    )

    # ========== Start the Processing ==========
    # Ensure response folder exists
    os.makedirs(result_folder, exist_ok=True)
    os.makedirs(project_result_folder, exist_ok=True)

    # Create a mapping dictionary
    file_mapping = {}

    # Scan the source folder for files
    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith(f".{file_extension}"):  # Only process Python files
                file_path = os.path.join(root, file)

                # Store relative path
                relative_path = os.path.relpath(file_path, src_folder.joinpath("..").resolve())

                # Store mapping
                file_mapping[relative_path] = file_path

    # Scan the test folder for files
    for root, _, files in os.walk(test_folder):
        for file in files:
            if file.endswith(f".{file_extension}"):  # Only process Python files
                file_path = os.path.join(root, file)

                # Store relative path
                relative_path = os.path.relpath(file_path, test_folder.joinpath("..").resolve())

                # Store mapping
                file_mapping[relative_path] = file_path
    
    # Save the mapping to a JSON file
    with open(json_mapping_file, "w") as json_file:
        json.dump(file_mapping, json_file, indent=4)

    logger.info(f"File mapping saved to {json_mapping_file}")

    text_prompt_template = Template(prompt.TEMPLATE_PROMPT)

    # Create the text prompt
    text_prompt = text_prompt_template.substitute(
        issue_id=issue.id,
        issue_title=issue.title,
        issue_summary=issue.summary,
        src_folder=issue.source_folder,
        test_folder=issue.test_folder,
        issue_log_report=issue.logs,
    )

    # Upload files to Gemini API and save responses in result folder
    for relative_path, file_path in file_mapping.items():

        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        if not file_content.strip():
            logger.warning(f"Skipping {relative_path} as it is empty.")
            continue

        response = model.generate_content(
            [
                text_prompt,
                file_content,
            ]
        )

        # Save response in results folder, preserving folder structure
        # Maintain the same structure
        result_file_path = os.path.join(project_result_folder, relative_path)

        # Create directories if needed
        os.makedirs(os.path.dirname(result_file_path), exist_ok=True)

        with open(result_file_path, "w", encoding="utf-8") as result_file:
            result_code = response.text
            if result_code.startswith(f"```{issue.programming_language}") and result_code.endswith("```"):
                result_code = result_code[len(f"```{issue.programming_language}"):-len("```")]
            result_file.write(result_code)

        logger.info(f"Processed {relative_path}, response saved to {result_file_path}")

    logger.info(f"All files uploaded and responses saved in the '{result_folder}'.")
