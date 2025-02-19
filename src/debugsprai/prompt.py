
TEMPLATE_PROMPT = """
I am providing you with multiple source code files in JSON format.
Please analyze and fix any error / hidden logic error, and also fix the related unit test according to the change in the source code.
We need to solve the issue based on following information. Analyse the file and check if there is any issue.
If the file empty, leave it as it is.
Comment the changes for fixed when necessary with AIFIX identification, it is show the changes are fixed by AI.
If the file is not empty, fix the code based on the following report:
* id: {issue_id}
* title: {issue_title}
* summary: {issue_summary}
* src_folder: {src_folder}
* test_folder: {test_folder}
* log_report: {issue_log_report}

Return only the corrected code in the exact same JSON format as below:
```json
{
    "source": [
        {
            "file_path": "relative/path/to/file.py",
            "code": "def some_function():\n    return True"
        },
        ...
    ],
    "test": [
        {
            "file_path": "relative/path/to/file.py",
            "code": "def test_something():\n    assert True"
        },
        ...
    ]
}
```
"""