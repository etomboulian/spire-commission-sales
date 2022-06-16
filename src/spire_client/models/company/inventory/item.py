from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Json


class Image(BaseModel):
    id: Optional[int]
    path: Optional[str]
    sequence: Optional[int]
    name: Optional[str]
    url: Optional[str]


class Links(BaseModel):
    components: str
    images: str
    serials: str
    upcs: str


class InventoryItem(BaseModel):
    id: Optional[int]
    whse: Optional[str]
    partNo: Optional[str]
    description: Optional[str]
    type: Optional[str]
    status: int
    lotNumbered: bool
    serialized: bool
    availableQty: Optional[str]
    onHandQty: Optional[str]
    committedQty: Optional[str]
    backorderQty: Optional[str]
    onPurchaseQty: Optional[str]
    foregroundColor: int
    backgroundColor: int
    primaryVendor: Optional[str]
    currentPONo: Optional[str]
    poDueDate: Optional[str]
    reorderPoint: Optional[str]
    minimumBuyQty: Optional[str]
    currentCost: Optional[str]
    averageCost: Optional[str]
    standardCost: Optional[str]
    buyMeasureCode: Optional[str]
    stockMeasureCode: Optional[str]
    sellMeasureCode: Optional[str]
    alternatePartNo: Optional[str]
    productCode: Optional[str]
    groupNo: Optional[str]
    salesDept: int
    userDef1: Optional[str]
    userDef2: Optional[str]
    discountable: bool
    weight: Optional[str]
    packSize: Optional[str]
    allowBackorders: bool
    allowReturns: bool
    dutyPct: Optional[str]
    freightPct: Optional[str]
    manufactureCountry: Optional[str]
    harmonizedCode: Optional[str]
    extendedDescription: Optional[str]
    unitOfMeasures: Dict[str, Any]
    pricing: Dict[str, Any]
    images: List[Image]
    defaultExpiryDate: int
    lotConsumeType: Optional[str]
    upload: bool
    lastModified: Optional[str]
    udf: Dict[str, Any]
    createdBy: Optional[str]
    modifiedBy: Optional[str]
    created: Optional[str]
    modified: Optional[str]
    links: Links
