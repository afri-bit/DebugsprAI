from pydantic import BaseModel
from pydantic import Field
from typing import Union, List


class Issue(BaseModel):
    id: Union[int, None] = Field(default=None)
    title: str = ""
    summary: str = ""
    severity_level: str = ""
    programming_language: str = ""
    project_folder: str = ""
    source_folder: str = ""
    test_folder: str = ""
    system_information: str = ""
    actual_behavior: str = ""
    expected_behavior: str = ""
    logs: str = ""


class Code(BaseModel):
    file_path: str
    code: str


class Project(BaseModel):
    source: List[Code]
    test: List[Code]
