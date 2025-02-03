
TEST_PROMPT = """
We need to solve the issue based on following information. Ananlyse the file and check if there is any issue.
If the file is not empty, fix the code based on the following information:
* id: {issue_id}
* title: {issue_title}
* description: {issue_description}
* type: {issue_type}
* src_folder: {src_folder}
* test_folder: {test_folder}
* log_report: {issue_log_report}

Requirements for the Output:
- No additional comment
- No markdown code annotations
- No markdown annotations
- The output must contain only the code with the same structures as the input code, but with the necessary fixes.
- Comment the changes for fixed when necessary with AIFIX identification.
"""