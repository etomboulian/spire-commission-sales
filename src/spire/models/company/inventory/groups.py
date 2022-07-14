from typing import List, Optional
from pydantic import BaseModel


class SalesDepartment(BaseModel):
    id: Optional[int]
    code: Optional[str]
    description: Optional[str]


class InventoryGroup(BaseModel):
    id: int
    code: Optional[str]
    description: str
    margin: str
    salesDepartment: SalesDepartment
    serviceCharge: str


class InventoryGroupList(BaseModel):
    records: List[InventoryGroup]
    start: int
    limit: int
    count: int
