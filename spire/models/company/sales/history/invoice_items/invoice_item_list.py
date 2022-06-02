
from datetime import date, datetime
from pydantic import BaseModel
from typing import Any, List, Optional


# /api/v2/companies/inspire2021/sales/invoice_items/
# Allows: [GET, HEAD, OPTIONS]

class Customer(BaseModel):
    customerNo: str
    name: str
    userDef2: str
    foregroundColor: int
    backgroundColor: int


class ShippingAddress(BaseModel):
    id: str
    name: str
    province: str


class Invoice(BaseModel):
    id: int
    territoryCode: Optional[str]
    salespersonNo: Optional[str]
    salespersonName: Optional[str]
    customerPO: Optional[str]
    shipDate: Optional[str]
    customer: Customer
    shippingAddress: ShippingAddress
    currency: str


class InvoiceItem(BaseModel):
    id: int
    invoiceNo: str
    recNo: int
    whse: str
    partNo: str
    itemType: int
    description: str
    invoiceDate: date
    orderQty: float
    committedQty: float
    backorderQty: float
    unitPrice: float
    extendedPrice: Optional[float]
    sellMeasure: str
    taxApplicable: List[bool]
    averageCost: Optional[float]
    averageMargin: Optional[float]
    currentCost: Optional[float]
    currentMargin: Optional[float]
    standardCost: Optional[float]
    standardMargin: Optional[float]
    lineDiscountPct: float
    discountPct: float
    inventoryGroupNo: Optional[str]
    requiredDate: Optional[str]
    invoice: Invoice
    employeeNo: Optional[str]
    promoCode: Optional[str]
    inventoryGL: str
    revenueGL: str
    costGL: str
    refNo: Optional[str]
    upcCode: str
    levyCode: Optional[str]
    jobNo: str
    jobAccountNo: Optional[str]
    comment: Optional[str]
    weight: str


class InvoiceItemList(BaseModel):
    records: List[InvoiceItem]
    start: int
    limit: int
    count: int
