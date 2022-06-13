from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel

# /api/v2/companies/inspire2021/sales/items/
# Allows: [GET, HEAD, OPTIONS]


class Customer(BaseModel):
    customerNo: str
    name: str
    foregroundColor: int
    backgroundColor: int


class ShippingAddress(BaseModel):
    shipId: str
    name: str
    line1: Optional[str]
    line2: str
    line3: str
    line4: str
    city: str
    postalCode: str
    shipCode: Optional[str]
    shipDescription: Optional[str]


class Order(BaseModel):
    id: int
    hold: bool
    status: str
    type: str
    orderDate: str
    customer: Customer
    customerPO: str
    invoiceNo: Any
    invoiceDate: Any
    batchNo: Any
    subtotal: str
    total: str
    baseTotal: str
    total2: str
    subTotal2: str
    backordered: bool
    grossProfit: Optional[str]
    grossProfitMargin: Optional[str]
    grossProfit2: Optional[str]
    totalCostCurrent: str
    totalCostAverage: str
    totalCostAverage2: str
    totalCostCurrent2: str
    shippingAddress: ShippingAddress
    fob: Optional[str]
    salespersonNo: Optional[str]
    division: str
    location: str
    territoryCode: Optional[str]
    shipCode: str
    requiredDate: Optional[str]
    shipDate: Optional[str]
    termsCode: str
    termsText: str
    referenceNo: Optional[str]
    currency: str
    modifiedBy: str
    createdBy: str
    created: str
    modified: str


class SalesOrderItem(BaseModel):
    id: int
    orderNo: str
    sequence: int
    whse: str
    partNo: str
    itemType: int
    description: str
    comment: Optional[str]
    orderQty: float
    committedQty: float
    backorderQty: float
    retailPrice: float
    lineDiscountPct: float
    discountPct: float
    unitPrice: float
    extendedPriceOrdered: str
    sellMeasure: str
    vendor: Optional[str]
    levyCode: Optional[str]
    inventoryGroupNo: Optional[str]
    requiredDate: Optional[str]
    suppress: bool
    averageCost: str
    currentCost: str
    standardCost: str
    weight: str
    employeeNo: Optional[str]
    jobNo: Optional[str]
    jobAccountNo: Optional[str]
    modifiedBy: str
    createdBy: str
    created: datetime
    modified: datetime
    order: Order


class SalesOrderItemList(BaseModel):
    records: List[SalesOrderItem]
    start: int
    limit: int
    count: int
