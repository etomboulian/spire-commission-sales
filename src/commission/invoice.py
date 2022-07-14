from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List

HOSTING_PRODUCT_CODE = ['HOSTING']
SUBSCRIPTION_PRODUCT_CODE = ['SUBSCRIP', 'SUBSA']


@dataclass
class InvoiceLine:
    invoice_no: str
    invoice_date: date
    salesperson_no: str
    part_no: str
    part_description: str
    inventory_group_no: str
    customer_no: str
    customer_name: str
    currency: str
    quantity: float
    amount: float = 0.0

    @property
    def hosting_sales(self):
        return self.amount if self.inventory_group_no in HOSTING_PRODUCT_CODE else 0

    @property
    def subscription_sales(self):
        return self.amount if self.inventory_group_no in SUBSCRIPTION_PRODUCT_CODE else 0


@dataclass
class Invoice:
    invoice_no: str
    salesperson_no: str
    customer_no: str
    lines: List[InvoiceLine] = field(default_factory=list)

    @property
    def hosting_sales(self):
        return sum([line.hosting_sales for line in self.lines])

    @property
    def subscription_sales(self):
        return sum([line.subscription_sales for line in self.lines])
