
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
    recNo: Optional[int]
    whse: Optional[str]
    partNo: Optional[str]
    itemType: int
    description: Optional[str]
    invoiceDate: Optional[date]
    orderQty: Optional[float]
    committedQty: Optional[float]
    backorderQty: Optional[float]
    unitPrice: Optional[float]
    extendedPrice: Optional[float]
    sellMeasure: Optional[str]
    taxApplicable: Optional[List[bool]]
    averageCost: Optional[float]
    averageMargin: Optional[float]
    currentCost: Optional[float]
    currentMargin: Optional[float]
    standardCost: Optional[float]
    standardMargin: Optional[float]
    lineDiscountPct: Optional[float]
    discountPct: Optional[float]
    inventoryGroupNo: Optional[str]
    requiredDate: Optional[str]
    invoice: Invoice
    employeeNo: Optional[str]
    promoCode: Optional[str]
    inventoryGL: Optional[str]
    revenueGL: Optional[str]
    costGL: Optional[str]
    refNo: Optional[str]
    upcCode: Optional[str]
    levyCode: Optional[str]
    jobNo: Optional[str]
    jobAccountNo: Optional[str]
    comment: Optional[str]
    weight: Optional[str]


class InvoiceItemList(BaseModel):
    records: List[InvoiceItem]
    start: int
    limit: int
    count: int
