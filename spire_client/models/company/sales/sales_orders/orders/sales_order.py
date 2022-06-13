from datetime import datetime
from typing import Dict, List
from typing import Any, List, Optional
from pydantic import BaseModel

# /api/v2/companies/inspire2021/sales/orders/{id}
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
    number: Optional[str]
    format: Optional[int]


class Fax(BaseModel):
    number: Optional[str]
    format: Optional[int]


class Salesperson(BaseModel):
    code: Optional[str]
    name: Optional[str]


class Territory(BaseModel):
    code: Optional[str]
    description: Optional[str]


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
    postalCode: Optional[str]
    provState: str
    country: str
    phone: Phone
    fax: Fax
    email: Optional[str]
    website: Optional[str]
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
    postalCode: Optional[str]
    provState: str
    country: str
    phone: Phone
    fax: Fax
    email: Optional[str]
    website: Optional[str]
    shipCode: Optional[str]
    shipDescription: Optional[str]
    salesperson: Salesperson
    territory: Territory
    sellLevel: int
    glAccount: Optional[str]
    defaultWarehouse: str
    udf: Any
    created: str
    modified: str
    contacts: List[Contact]
    salesTaxes: List[SalesTax]


class Contact2(BaseModel):
    name: Any
    email: Any
    phone: Phone
    fax: Fax


class Tax(BaseModel):
    code: Optional[int]
    name: Optional[str]
    shortName: Optional[str]
    rate: float
    exemptNo: Optional[str]
    total: Optional[float]


class Inventory(BaseModel):
    id: int
    whse: str
    partNo: str
    description: str


class Item(BaseModel):
    id: int
    orderNo: str
    sequence: int
    parentSequence: int
    inventory: Optional[Inventory]
    serials: Any
    whse: str
    partNo: str
    description: str
    comment: Any
    orderQty: float
    committedQty: float
    backorderQty: float
    sellMeasure: Optional[str]
    retailPrice: float
    unitPrice: float
    userPrice: bool
    discountable: bool
    discountPct: float
    discountAmt: float
    taxFlags: List[bool]
    vendor: Optional[str]
    levyCode: Any
    requiredDate: Optional[str]
    extendedPriceOrdered: str
    extendedPriceCommitted: str
    kit: bool
    suppress: bool
    udf: Dict[str, Any]


class Links(BaseModel):
    notes: str


class SalesOrder(BaseModel):
    id: int
    orderNo: str
    division: str
    location: str
    profitCenter: Any
    invoiceNo: Any
    customer: Customer
    creditApprovedAmount: str
    creditApprovedDate: Any
    creditApprovedUser: Any
    currency: Currency
    status: str
    type: str
    hold: bool
    orderDate: str
    invoiceDate: Any
    requiredDate: str
    recurrenceRule: Any
    address: Address
    shippingAddress: ShippingAddress
    contact: Contact2
    customerPO: Optional[str]
    batchNo: Any
    fob: Optional[str]
    incoterms: Optional[str]
    incotermsPlace: Optional[str]
    referenceNo: Optional[str]
    shippingCarrier: Optional[str]
    shipDate: Optional[datetime]
    trackingNo: Optional[str]
    termsCode: str
    termsText: str
    freight: str
    taxes: List[Tax]
    subtotal: str
    subtotalOrdered: str
    discount: str
    totalDiscount: str
    total: str
    totalOrdered: str
    grossProfit: str
    items: List[Item]
    payments: List
    udf: Dict[str, Any]
    createdBy: str
    modifiedBy: str
    created: str
    modified: str
    deletedBy: Any
    deleted: Any
    links: Links
