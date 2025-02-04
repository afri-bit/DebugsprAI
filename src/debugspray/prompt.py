
TEMPLATE_PROMPT = """
We need to solve the issue based on following information. Analyse the file and check if there is any issue.
If the file is not empty, fix the code based on the following report:
* id: {issue_id}
* title: {issue_title}
* description: {issue_description}
* src_folder: {src_folder}
* test_folder: {test_folder}
* log_report: {issue_log_report}

Requirements for the Output:
- Output only raw code.
- Do not use markdown formatting, backticks, or any annotations.
- Do not wrap the code inside code blocks.
- Do not add explanations, comments, or extra text.
- Just return the plain executable code.
- Output code must be in the same structure as the input code with the necessary fixes
- Comment the changes for fixed when necessary with AIFIX identification.
"""