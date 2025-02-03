

from pydantic import BaseModel

class Issue(BaseModel):
    id: int
    title: str
    description: str
    status: str
    src: str
    log: str


class Output(BaseModel):
    result_status: str
