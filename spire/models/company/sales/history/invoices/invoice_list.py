from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# /api/v2/companies/inspire2021/sales/invoices/
# Allows: [GET, HEAD, OPTIONS, POST]


class Customer(BaseModel):
    id: int
    customerNo: str
    name: str
    userDef2: str
    invoiceType: str
    foregroundColor: int
    backgroundColor: int


class Address(BaseModel):
    id: int
    line1: str
    line2: str
    line3: str
    line4: str
    city: Optional[str]
    provState: Optional[str]
    postalCode: Optional[str]
    country: Optional[str]


class ShippingAddress(BaseModel):
    id: int
    shipId: str
    name: str
    line1: str
    line2: str
    line3: str
    line4: str
    city: str
    provState: Optional[str]
    postalCode: Optional[str]
    country: Optional[str]
    shipCode: Optional[str]
    shipDescription: Optional[str]


class Phone(BaseModel):
    number: Optional[str]
    format: int


class Fax(BaseModel):
    number: Optional[str]
    format: int


class Contact(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Phone
    fax: Fax


class Links(BaseModel):
    self: str


class Invoice(BaseModel):
    id: int
    invoiceNo: str
    invoiceDate: datetime
    customer: Customer
    orderNo: str
    orderDate: datetime
    total: str
    baseTotal: str
    grossProfit: str
    grossProfitMargin: Optional[str]
    transNo: str
    division: str
    location: str
    profitCenter: Optional[str]
    fob: Optional[str]
    incoterms: Optional[str]
    incotermsPlace: Optional[str]
    referenceNo: Optional[str]
    discount: str
    totalDiscount: str
    totalCostAverage: str
    totalCostCurrent: str
    totalCostStandard: str
    termsCode: str
    termsText: str
    customerPO: Optional[str]
    salespersonNo: Optional[str]
    salespersonName: Optional[str]
    subTotal: str
    territoryCode: Optional[str]
    freight: str
    weight: str
    shipDate: Optional[str]
    shippingCarrier: Optional[str]
    trackingNo: Optional[str]
    requiredDate: Optional[str]
    wasQuoteNo: Optional[str]
    jobNo: str
    jobAccountNo: Optional[str]
    invoicedUser: str
    currency: str
    address: Address
    shippingAddress: ShippingAddress
    contact: Contact
    createdBy: str
    modifiedBy: str
    created: datetime
    modified: datetime
    links: Links


class InvoiceList(BaseModel):
    records: List[Invoice]
    start: int
    limit: int
    count: int
