from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel


class Territory(BaseModel):
    id: int
    code: str
    name: Optional[str]
    description: Optional[str]
    created: Optional[datetime]
    createdBy: Optional[str]
    modified: Optional[str]
    modifiedBy: Optional[datetime]


class TerritoryList(BaseModel):
    records: List[Territory]
    start: int
    limit: int
    count: int
