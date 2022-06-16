
from datetime import datetime
from typing import Dict, List
from typing import Any, List, Optional
from pydantic import BaseModel

# /api/v2/companies/inspire2021/sales/invoices/{id}
# Allows: [GET, HEAD, PUT, DELETE, OPTIONS]


class Customer(BaseModel):
    id: int
    code: str
    customerNo: str
    name: str


class Currency(BaseModel):
    id: int
    code: str
    description: str
    country: str
    units: str
    fraction: str
    symbol: str
    decimalPlaces: int
    symbolPosition: str
    rate: str
    rateMethod: str
    glAccountNo: str
    thousandsSeparator: str
    lastYearRate: List[str]
    thisYearRate: List[str]
    nextYearRate: List[str]


class Phone(BaseModel):
    number: str
    format: int


class Fax(BaseModel):
    number: str
    format: int


class Salesperson(BaseModel):
    code: str
    name: str


class Territory(BaseModel):
    code: str
    description: str


class Contact(BaseModel):
    name: str
    email: str
    phone: Phone
    fax: Fax


class SalesTax(BaseModel):
    code: int
    exempt: str


class Address(BaseModel):
    id: int
    type: str
    linkTable: str
    linkType: str
    linkNo: str
    shipId: str
    name: str
    line1: str
    line2: str
    line3: str
    line4: str
    city: str
    postalCode: str
    provState: str
    country: str
    phone: Phone
    fax: Fax
    email: str
    website: str
    shipCode: str
    shipDescription: str
    salesperson: Salesperson
    territory: Territory
    sellLevel: int
    glAccount: str
    defaultWarehouse: str
    udf: Any
    created: str
    modified: str
    contacts: List[Contact]
    salesTaxes: List[SalesTax]


class ShippingAddress(BaseModel):
    id: int
    type: str
    linkTable: str
    linkType: str
    linkNo: str
    shipId: str
    name: str
    line1: str
    line2: str
    line3: str
    line4: str
    city: str
    postalCode: str
    provState: str
    country: str
    phone: Phone
    fax: Fax
    email: str
    website: str
    shipCode: str
    shipDescription: str
    salesperson: Salesperson
    territory: Territory
    sellLevel: int
    glAccount: str
    defaultWarehouse: str
    udf: Any
    created: str
    modified: str
    contacts: List[Contact]
    salesTaxes: List[SalesTax]


class Tax(BaseModel):
    code: int
    name: str
    shortName: str
    rate: str
    exemptNo: str
    total: str


class Inventory(BaseModel):
    id: int
    whse: str
    partNo: str
    description: str


class Item(BaseModel):
    id: int
    invoiceNo: str
    sequence: int
    inventory: Optional[Inventory]
    whse: str
    partNo: str
    description: str
    comment: Optional[str]
    orderQty: str
    committedQty: str
    backorderQty: str
    retailPrice: str
    unitPrice: str
    lineDiscountPct: str
    discountPct: str
    taxFlags: List[bool]
    sellMeasure: str
    extendedPriceOrdered: str
    extendedPriceCommitted: str
    udf: Dict[str, Any]


class Links(BaseModel):
    notes: str


class Invoice(BaseModel):
    id: int
    invoiceNo: str
    orderNo: str
    division: str
    location: str
    profitCenter: Optional[str]
    customer: Customer
    currency: Currency
    orderDate: str
    invoiceDate: datetime
    requiredDate: Optional[str]
    address: Address
    shippingAddress: ShippingAddress
    customerPO: Optional[str]
    fob: str
    incoterms: Optional[str]
    incotermsPlace: Optional[str]
    referenceNo: Optional[str]
    shippingCarrier: Optional[str]
    shipDate: Optional[str]
    trackingNo: Optional[str]
    termsCode: str
    termsText: str
    freight: str
    taxes: List[Tax]
    subtotal: str
    total: str
    items: List[Item]
    payments: List
    udf: Dict[str, Any]
    createdBy: str
    modifiedBy: str
    created: datetime
    modified: datetime
    links: Links
