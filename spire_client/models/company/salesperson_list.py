from datetime import datetime
from typing import List
from pydantic import BaseModel


class Salesperson(BaseModel):
    id: int
    salespersonNo: str
    code: str
    name: str
    created: datetime
    createdBy: str
    modified: datetime
    modifiedBy: str


class SalespersonList(BaseModel):
    records: List[Salesperson]
    start: int
    limit: int
    count: int
