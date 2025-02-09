import json
import os
import pathlib
from string import Template

import google.generativeai as genai

import debugsprai.logger as logger
import debugsprai.prompt as prompt
from debugsprai.models import Issue

logger = logger.setup_logger(__name__)


def debug_issue(project_path: str, issue_file_path: str, result_folder: str="results"):
    # Parse the issue file
    issue: Issue | None = None
    try:
        with open(issue_file_path, "r") as file:
            file_data = json.load(file)  # Load JSON from file

            issue = Issue.model_validate(file_data)
            logger.info(f"Loaded issue: {issue}")
    except Exception as e:
        logger.error(f"Failed to load issue: {e}")

    # Configuration the project path
    if not os.path.exists(project_path):
        logger.error(f"Project path does not exist: '{project_path}'")
        return
    # Get the additional path from the issue file
    project_path = pathlib.Path(project_path).absolute().resolve()
    src_folder = project_path.joinpath(issue.src).resolve()
    result_folder = pathlib.Path(result_folder).absolute().resolve()
    JSON_MAPPING_FILE = "file_mapping.json"

    # ========== Google Gemini Configuration ==========
    # Configure API Key
    GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME") or "gemini-2.0-flash-exp"
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if GEMINI_API_KEY is None:
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
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    # ========== Start the Processing ==========
    # Ensure response folder exists
    os.makedirs(result_folder, exist_ok=True)

    # Create a mapping dictionary
    file_mapping = {}

    # Step 1: Scan the src folder for Python files
    for root, _, files in os.walk(src_folder):
        for file in files:
            # TODO: Add support for other file types (dynamic configuration)
            if file.endswith(".py"):  # Only process Python files
                file_path = os.path.join(root, file)

                # Store relative path
                relative_path = os.path.relpath(file_path, src_folder)

                # Store mapping
                file_mapping[relative_path] = file_path

    # Step 2: Save the mapping to a JSON file
    with open(JSON_MAPPING_FILE, "w") as json_file:
        json.dump(file_mapping, json_file, indent=4)

    logger.info(f"File mapping saved to {JSON_MAPPING_FILE}")

    text_prompt_template = Template(prompt.TEMPLATE_PROMPT)

    # Create the text prompt
    text_prompt = text_prompt_template.substitute(
        issue_id=issue.id,
        issue_title=issue.title,
        issue_description=issue.description,
        src_folder=issue.src,
        test_folder=issue.test,
        issue_log_report=issue.log,
    )

    # Step 3: Upload files to Gemini API and save responses in result folder
    for relative_path, file_path in file_mapping.items():

        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        if not file_content.strip():
            logger.warning(f"Skipping {relative_path} as it is empty.")
            continue

        model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp",
                                      generation_config=generation_config)

        response = model.generate_content(
            [
                text_prompt,
                file_content,
            ]
        )

        # Step 4: Save response in results folder, preserving folder structure
        # Maintain the same structure
        result_file_path = os.path.join(result_folder, relative_path)

        # Create directories if needed
        os.makedirs(os.path.dirname(result_file_path), exist_ok=True)

        with open(result_file_path, "w", encoding="utf-8") as result_file:
            result_file.write(response.text)

        logger.info(f"Processed {relative_path}, response saved to {result_file_path}")

    logger.info(f"All files uploaded and responses saved in the '{result_folder}'.")
