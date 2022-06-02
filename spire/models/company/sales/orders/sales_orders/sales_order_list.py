from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel

# /api/v2/companies/inspire2021/sales/orders/
# Allows: [GET, HEAD, OPTIONS, POST]


class Customer(BaseModel):
    id: Optional[int]
    customerNo: Optional[str]
    name: Optional[str]
    userDef2: Optional[str]
    invoiceType: Optional[str]
    hold: Optional[bool]
    foregroundColor: Optional[str]
    backgroundColor: Optional[str]


class Address(BaseModel):
    id: Optional[int]
    line1: Optional[str]
    line2: Optional[str]
    line3: Optional[str]
    line4: Optional[str]
    city: Optional[str]
    provState: Optional[str]
    postalCode: Optional[str]
    country: Optional[str]


class ShippingAddress(BaseModel):
    id: Optional[int]
    shipId: Optional[str]
    name: Optional[str]
    line1: Optional[str]
    line2: Optional[str]
    line3: Optional[str]
    line4: Optional[str]
    city: Optional[str]
    provState: Optional[str]
    postalCode: Optional[str]
    country: Optional[str]
    shipCode: Optional[str]
    shipDescription: Optional[str]


class Phone(BaseModel):
    number: Optional[str]
    format: Optional[int]


class Fax(BaseModel):
    number: Optional[str]
    format: Optional[int]


class Contact(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[Phone]
    fax: Optional[Fax]


class Links(BaseModel):
    self: str


class SalesOrderSummary(BaseModel):
    id: int
    orderNo: str
    invoiceNo: Optional[str]
    customer: Customer
    status: str
    type: str
    hold: bool
    orderDate: str
    invoiceDate: Optional[str]
    requiredDate: Optional[str]
    customerPO: Optional[str]
    batchNo: Optional[str]
    division: str
    location: str
    profitCenter: Optional[str]
    fob: Optional[str]
    incoterms: Optional[str]
    incotermsPlace: Optional[str]
    salespersonNo: Optional[str]
    territoryCode: Optional[str]
    freight: float
    weight: float
    discount: float
    totalDiscount: float
    subtotal: float
    total: float
    baseTotal: float
    total2: float
    totalOrdered: float
    subtotalOrdered: float
    backordered: bool
    totalBackorderQty: Optional[float]
    grossProfit: float
    grossProfitMargin: Optional[float]
    grossProfit2: float
    totalCostAverage: float
    totalCostAverage2: float
    totalCostCurrent: float
    totalCostCurrent2: float
    totalCostStandard: float
    totalCostStandard2: float
    phaseId: str
    termsCode: str
    termsText: str
    referenceNo: Optional[str]
    currency: str
    shippingCarrier: Optional[str]
    shipDate: Optional[str]
    trackingNo: Optional[str]
    jobNo: Optional[str]
    jobAccountNo: Optional[str]
    wasQuoteNo: Optional[str]
    amountPaid: Optional[float]
    amountUnpaid: Optional[float]
    amountUnpaidOrdered: Optional[float]
    percentPaid: Optional[float]
    address: Address
    shippingAddress: ShippingAddress
    contact: Contact
    created: Optional[datetime]
    createdBy: str
    modified: Optional[datetime]
    modifiedBy: str
    deleted: Optional[datetime]
    deletedBy: Optional[str]
    links: Links


class SalesOrderList(BaseModel):
    records: List[SalesOrderSummary]
    start: int
    limit: int
    count: int
