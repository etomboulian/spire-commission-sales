from datetime import date
from typing import Any, List, Optional
from pydantic import BaseModel


class SalesDepartment(BaseModel):
    id: Optional[int]
    code: Optional[str]


class Pricing(BaseModel):
    sellPrice: List[float]
    currMargin: Optional[float]
    currMarginPct: Optional[float]
    avgMargin: Optional[float]
    avgMarginPct: Optional[float]


class Uom(BaseModel):
    description: Optional[str]
    location: Optional[str]
    weight: Optional[str]


class Levy(BaseModel):
    code: Optional[str]


class PrimaryVendor(BaseModel):
    vendorNo: Optional[str]


class Links(BaseModel):
    self: str


class InventoryItem(BaseModel):
    id: int
    whse: Optional[str]
    partNo: Optional[str]
    description: Optional[str]
    status: int
    availableQty: Optional[str]
    onHandQty: Optional[str]
    backorderQty: Optional[str]
    committedQty: Optional[str]
    onPurchaseQty: Optional[str]
    buyMeasureCode: Optional[str]
    stockMeasureCode: Optional[str]
    sellMeasureCode: Optional[str]
    alternatePartNo: Optional[str]
    currentCost: Optional[float]
    averageCost: Optional[float]
    standardCost: Optional[float]
    groupNo: Optional[str]
    type: Optional[str]
    salesDepartment: Optional[SalesDepartment]
    userDef1: Optional[str]
    userDef2: Optional[str]
    poDueDate: Optional[date]
    currentPONo: Optional[str]
    reorderPoint: Optional[str]
    minimumBuyQty: Optional[str]
    lastYearQty: Optional[str]
    lastYearSales: Optional[str]
    thisYearQty: Optional[str]
    thisYearSales: Optional[str]
    nextYearQty: Optional[str]
    nextYearSales: Optional[str]
    allowBackorders: bool
    allowReturns: bool
    dutyPct: Optional[str]
    freightPct: Optional[str]
    defaultExpiryDate: Optional[int]
    lotConsumeType: Optional[str]
    manufactureCountry: Optional[str]
    harmonizedCode: Optional[str]
    suggestedOrderQty: Optional[str]
    pricing: Pricing
    uom: Optional[Uom]
    packSize: Optional[str]
    foregroundColor: int
    backgroundColor: int
    levy: Optional[Levy]
    primaryVendor: Optional[PrimaryVendor]
    allowBackOrders: bool
    dfltExpiryDays: Optional[int]
    mfgCountry: Optional[str]
    hsCode: Optional[str]
    serializedMode: Optional[str]
    upload: bool
    lastModified: Optional[str]
    lastSaleDate: Optional[str]
    lastReceiptDate: Optional[str]
    lastCountDate: Optional[str]
    lastCountQty: Optional[str]
    lastCountVariance: Optional[str]
    created: Optional[str]
    createdBy: Optional[str]
    modified: Optional[str]
    modifiedBy: Optional[str]
    links: Links


class InventoryItemList(BaseModel):
    records: List[InventoryItem]
    start: int
    limit: int
    count: int
