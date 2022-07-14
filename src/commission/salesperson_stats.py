from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List
from .invoice import Invoice


@dataclass
class SalespersonStats:
    salesperson_no: str
    invoices: List[Invoice] = field(default_factory=list)

    @property
    def hosting_sales(self):
        return sum([invoice.hosting_sales for invoice in self.invoices])

    @property
    def subscription_sales(self):
        return sum([invoice.subscription_sales for invoice in self.invoices])
