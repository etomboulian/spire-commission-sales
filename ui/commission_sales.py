import sys
import csv
from datetime import datetime
from dataclasses import dataclass, field
from typing import List

from spire import Server as ApiClient


@dataclass
class InvoiceLine:
    invoice_no: str
    territory_code: str
    part_no: str
    customer_no: str
    amount: float = 0.0


@dataclass
class Invoice:
    invoice_no: str
    customer_no: str
    lines: List[InvoiceLine] = field(default_factory=list)

    @property
    def hosting_sales(self):
        return sum([line.amount for line in self.lines if line.part_no == 'HOSTING'])

    @property
    def subscription_sales(self):
        return sum([line.amount for line in self.lines if line.part_no == 'SUBSCRIPTION'])


@dataclass
class TerritoryCustomerStats:
    territory_code: str
    customer_no: str
    invoices: List[Invoice] = field(default_factory=list)

    @property
    def hosting_sales(self):
        return sum([invoice.hosting_sales for invoice in self.invoices])

    @property
    def subscription_sales(self):
        return sum([invoice.subscription_sales for invoice in self.invoices])


class CommissionSales:
    def __init__(self, api_client, start_date, end_date, trial=None):
        self.start_date = start_date
        self.end_date = end_date
        self.api_client = api_client
        self.territory_sales_stats = list()

    def post_commissions(self, post_date, commission_rate, trial=None):
        history_items = self.api_client.SalesHistoryItems.all()

        # Filter list of all items to only include invoice items where the product is either HOSTING or SUBSCRIPTION
        filtered_items = list(
            filter(lambda x:
                   (x.partNo == 'HOSTING' or x.partNo == 'SUBSCRIPTION')
                   and x.invoiceDate >= self.start_date and x.invoiceDate <= self.end_date, history_items
                   )
        )

        # Create territory customer stats from the list of items filtered to HOSTING or SUBSCRIPTION
        self.create_territory_customer_stats(filtered_items)

        result = []

        for i in self.territory_sales_stats:
            sales_order = {}
            sales_order['customer'] = {}
            sales_order['customer']['customerNo'] = i.territory_code

            #new_order = self.api_client.SalesOrders.new(sales_order)

            sales_order['referenceNo'] = 'Commission'
            sales_order['items'] = []

            if i.hosting_sales > 0:
                line_item = {}
                line_item['partNo'] = 'HOSTINGCOMM'
                line_item['orderQty'] = -1
                line_item['unitPrice'] = (i.hosting_sales * commission_rate)
                line_item[
                    'description'] = f'Credit for Server Hosting sales for customer {i.customer_no}'
                sales_order['items'].append(line_item)

            if i.subscription_sales > 0:
                line_item = {}
                line_item['partNo'] = 'SUBSCRIPCOM'
                line_item['orderQty'] = -1
                line_item['unitPrice'] = (
                    i.subscription_sales * commission_rate)
                line_item[
                    'description'] = f'Credit for Subscription sales for customer {i.customer_no}'
                sales_order.items.append(line_item)

            result.append(sales_order)

        with open('output.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'customer_no', 'reference',
                            'partNo', 'orderQty', 'unitPrice', 'description'])
            for i, row in enumerate(result):

                result_row_prefix = [i, row['customer']
                                     ['customerNo'], row['referenceNo']]
                for item in row['items']:
                    result_row = result_row_prefix.copy()
                    result_row.extend(
                        [item['partNo'], item['orderQty'], item['unitPrice'], item['description']])
                    writer.writerow(result_row)

        if not trial:
            for item in result:
                self.api_client.SalesOrders.new(item)

        if len(result) <= 0:
            msg = 'No items found to post commissions for'
        elif trial:
            msg = 'Commission Orders saved to output.csv'
        else:
            msg = 'Commission Sales Orders Posted Successfully'
        return msg

    def create_territory_customer_stats(self, item_list):
        # Get a list of all salespeople and customers from the filtered list
        # Use a set so that duplicate combinations of territory and customer are ignored
        territory_customers = (
            [item.invoice.territoryCode, item.invoice.customer.customerNo] for item in item_list)

        # For each territory and customer combination create a territory_customer stats object
        for territory_code, customer_no in territory_customers:
            territory_sales_stat = TerritoryCustomerStats(
                territory_code=territory_code, customer_no=customer_no)
            self.territory_sales_stats.append(territory_sales_stat)

        # For each territory_sales stats item that exists
        for stats_item in self.territory_sales_stats:
            # Get a list of the relevant data from the invoice lines that belong to this territory and customer
            invoice_line_list = [
                [item.invoiceNo, item.invoice.territoryCode,
                    item.invoice.customer.customerNo, item.partNo, item.extendedPrice]
                for item in item_list
                if item.invoice.territoryCode == stats_item.territory_code
                and item.invoice.customer.customerNo == stats_item.customer_no
            ]

            # Get a list of the invoiceNo and customerNo in the list to process
            invoices = ([line[0], line[2]] for line in invoice_line_list)

            for invoice_number, customer_no in invoices:
                # Create a new invoice
                _invoice = Invoice(invoice_no=invoice_number,
                                   customer_no=customer_no)

                # Get the data to fill this invoices lines with
                this_invoice_lines = [
                    line for line in invoice_line_list if line[0] == _invoice.invoice_no]

                for line in this_invoice_lines:
                    # Create a new invoice line and add it to the current invoice
                    invoice_line = InvoiceLine(
                        invoice_no=line[0], territory_code=line[1], customer_no=line[2], part_no=line[3], amount=line[4])
                    _invoice.lines.append(invoice_line)

                # Add the current invoice into the stats_item for this territory and customer combination
                stats_item.invoices.append(_invoice)


def create_commission_sales_orders(api_client, start_date, end_date, post_date, commission_rate, trial=None):
    commission_rate = float(commission_rate)

    commission_sales = CommissionSales(
        api_client, start_date=start_date, end_date=end_date)
    result = commission_sales.post_commissions(
        post_date=post_date, commission_rate=commission_rate, trial=trial)
    return result


if __name__ == '__main__':
    create_commission_sales_orders(
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
