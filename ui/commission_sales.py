import sys
import csv
from datetime import datetime
from dataclasses import dataclass, field
from typing import List

from spire_client.models.company import salesperson_list


HOSTING_PRODUCT_CODE = 'HOSTING'
HOSTING_COMMISSION_RATE = 0.20

SUBSCRIPTION_PRODUCT_CODE = 'SUBSCRIP'
SUBSCRIPTION_COMMISSION_RATE = 0.25


@dataclass
class InvoiceLine:
    invoice_no: str
    salesperson_no: str
    part_no: str
    part_description: str
    inventory_group_no: str
    customer_no: str
    customer_name: str
    amount: float = 0.0

    @property
    def hosting_sales(self):
        return self.amount if self.inventory_group_no == HOSTING_PRODUCT_CODE else 0

    @property
    def subscription_sales(self):
        return self.amount if self.inventory_group_no == SUBSCRIPTION_PRODUCT_CODE else 0


@dataclass
class Invoice:
    invoice_no: str
    salesperson_no: str
    customer_no: str
    lines: List[InvoiceLine] = field(default_factory=list)

    @property
    def hosting_sales(self):
        return sum([line.amount for line in self.lines if line.inventory_group_no == 'HOSTING'])

    @property
    def subscription_sales(self):
        return sum([line.amount for line in self.lines if line.inventory_group_no == 'SUBSCRIP'])


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


class CommissionSales:
    def __init__(self, api_client, start_date, end_date, trial=None):
        self.start_date = start_date
        self.end_date = end_date
        self.api_client = api_client
        self.salesperson_stats_list = list()
        self.comission_orders_list = list()

    def post_commission_sales_orders(self, post_date, trial=None):

        # Get the partNos to call invoices with
        inventory_filter_obj = {
            "$or": [
                {"groupNo": f"{SUBSCRIPTION_PRODUCT_CODE}"},
                {"groupNo": f"{HOSTING_PRODUCT_CODE}"}
            ]
        }

        commission_parts = self.api_client.InventoryItems.all(
            filter=inventory_filter_obj)
        commission_parts_part_nos = [item.partNo for item in commission_parts]

        # Setup a Filter on the part number in the API Call to get invoice items
        order_filter_obj = {
            "invoiceDate": {"$gte": self.start_date.strftime('%y-%m-%d')},
            "$or": [],

        }

        # Populate the filter object with the parts retrieved
        for part_no in commission_parts_part_nos:
            order_filter_obj['$or'].append({"partNo": f"{part_no}"})

        invoice_items_list = self.api_client.SalesHistoryItems.all(
            filter=order_filter_obj)

        # Filter list of all items locally to only include invoiced items in the selected date range
        filtered_invoice_items = list(
            filter(
                lambda x: x.invoiceDate >= self.start_date and x.invoiceDate <= self.end_date,
                invoice_items_list
            )
        )

        self.salesperson_stats_list = CommissionSales.create_salesperson_stats(
            filtered_invoice_items)

        self.commission_orders_list = self.generate_commission_orders(
            self.salesperson_stats_list, post_date)

        if not trial:
            self.create_spire_sales_orders(self.commission_orders_list)

        CommissionSales.write_results_to_csv(self.commission_orders_list)
        msg = CommissionSales.check_results(self.commission_orders_list, trial)

        return msg

    def create_salesperson_stats(invoice_items_list):
        # Populate this array and return it
        salesperson_stats_list = []

        # Generate the invoice line item objects collection
        invoice_lines = []
        for invoice_item in invoice_items_list:

            # Filter out null values of salespersonNo received
            if invoice_item.invoice.salespersonNo:
                line = InvoiceLine(
                    invoice_no=invoice_item.invoiceNo,
                    salesperson_no=invoice_item.invoice.salespersonNo,
                    part_no=invoice_item.partNo,
                    part_description=invoice_item.description,
                    inventory_group_no=invoice_item.inventoryGroupNo,
                    customer_no=invoice_item.invoice.customer.customerNo,
                    customer_name=invoice_item.invoice.customer.name,
                    amount=invoice_item.extendedPrice
                )
                invoice_lines.append(line)

        # Generate the invoice objects collection
        invoices = []
        for line in invoice_lines:
            if existing_invoice := next(filter(lambda x: x.invoice_no == line.invoice_no, invoices), None):
                existing_invoice.lines.append(line)
            else:
                new_invoice = Invoice(
                    line.invoice_no, line.salesperson_no, line.customer_no)
                new_invoice.lines.append(line)
                invoices.append(new_invoice)

        # Generate the salesperson_stats_list data
        for invoice in invoices:
            if existing_stats_record := next(filter(lambda x: x.salesperson_no == invoice.salesperson_no, salesperson_stats_list), None):
                existing_stats_record.invoices.append(invoice)
            else:
                new_stats_record = SalespersonStats(invoice.salesperson_no)
                new_stats_record.invoices.append(invoice)
                salesperson_stats_list.append(new_stats_record)

        salesperson_stats_list.sort(key=lambda x: x.salesperson_no)
        return salesperson_stats_list

    def generate_commission_orders(self, salesperson_stats_list, post_date):
        spire_commission_orders = []
        print("Summary -------")
        for salesperson in salesperson_stats_list:
            new_sales_order = {}
            new_sales_order['customer'] = {}
            new_sales_order['customer']['customerNo'] = salesperson.salesperson_no
            new_sales_order['orderDate'] = post_date.strftime('%Y-%m-%d')
            new_sales_order['referenceNo'] = 'Commission App Entry'
            new_sales_order['items'] = []

            print(salesperson.salesperson_no, round(salesperson.hosting_sales + salesperson.subscription_sales, 2),
                  round((salesperson.hosting_sales * HOSTING_COMMISSION_RATE) + (salesperson.subscription_sales * SUBSCRIPTION_COMMISSION_RATE), 2))

            for invoice in salesperson.invoices:
                for item in invoice.lines:
                    if item.hosting_sales != 0:
                        line_item = {}
                        line_item['partNo'] = 'SUBHOST'
                        line_item['orderQty'] = -1
                        line_item['unitPrice'] = round(
                            (item.hosting_sales * HOSTING_COMMISSION_RATE), 2)
                        line_item[
                            'comment'] = f'Commission for: {item.part_no} | {item.part_description} | {item.customer_name}'
                        #f'Commission for Hosting | Customer: {item.customer_name} | InvoiceNo: {item.invoice_no} | partNo: {item.part_no}'
                        new_sales_order['items'].append(line_item)

                    if item.subscription_sales != 0:
                        line_item = {}
                        line_item['partNo'] = 'SUBCOMM'
                        line_item['orderQty'] = -1
                        line_item['unitPrice'] = round(
                            (item.subscription_sales * SUBSCRIPTION_COMMISSION_RATE), 2)
                        line_item[
                            'comment'] = f'Commission for: {item.part_no} | {item.part_description} | {item.customer_name}'
                        #f'Commission for Subscription | Customer: {item.customer_name} | InvoiceNo: {item.invoice_no} | partNo: {item.part_no}'
                        new_sales_order['items'].append(line_item)

            spire_commission_orders.append(new_sales_order)

        return spire_commission_orders

    def create_spire_sales_orders(self, commission_orders_list):
        for order in commission_orders_list:
            self.api_client.SalesOrders.new(order)

    def write_results_to_csv(commission_orders_list):
        with open('output.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'customer_no', 'reference',
                            'partNo', 'orderQty', 'unitPrice', 'description'])
            for i, row in enumerate(commission_orders_list):

                result_row_prefix = [i, row['customer']
                                     ['customerNo'], row['referenceNo']]
                for item in row['items']:
                    result_row = result_row_prefix.copy()
                    result_row.extend(
                        [item['partNo'], item['orderQty'], item['unitPrice'], item['comment']])
                    writer.writerow(result_row)

    def check_results(commission_orders_list, trial):
        if len(commission_orders_list) <= 0:
            msg = 'No items found to post commissions for'
        elif trial:
            msg = 'Commission Orders saved to output.csv'
        else:
            msg = 'Commission Sales Orders Posted Successfully'
        return msg


def create_commission_sales_orders(api_client, start_date, end_date, post_date, trial=None):

    commission_sales = CommissionSales(
        api_client, start_date=start_date, end_date=end_date)
    result = commission_sales.post_commission_sales_orders(
        post_date=post_date, trial=trial)
    return result


if __name__ == '__main__':
    create_commission_sales_orders(
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
