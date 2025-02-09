from pydantic import BaseModel
from pydantic import Field
from typing import Union


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
