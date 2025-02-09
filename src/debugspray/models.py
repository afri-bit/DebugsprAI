from pydantic import BaseModel
from pydantic import Field


class Issue(BaseModel):
    id: int
    title: str
    description: str
    severity_level: str = Field(default="")
    actual_behavior: str = Field(default="")
    expected_behavior: str = Field(default="")
    system_information: str = Field(default="")
    source_folder: str = Field(default="src")
    test_folder: str = Field(default="test")
    log: str


class Output(BaseModel):
    result_status: str
