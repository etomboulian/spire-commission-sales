import sys
import csv
from datetime import date, datetime
from dataclasses import dataclass, field
from typing import List
from .invoice import Invoice, InvoiceLine
from .salesperson_stats import SalespersonStats

HOSTING_PRODUCT_CODE = ['HOSTING']
SUBSCRIPTION_PRODUCT_CODE = ['SUBSCRIP', 'SUBSA']


class CommissionSales:
    def __init__(self, api_client, start_date, end_date, trial=None):
        self.start_date = start_date
        self.end_date = end_date
        self.api_client = api_client
        self.salesperson_stats_list = list()
        self.comission_orders_list = list()

    def post_commission_sales_orders(self, post_date, trial=None):
        commissionable_invoice_items = self.get_commissionable_invoice_items()

        filtered_commissionable_invoice_items = self.filter_commissionable_invoice_items_by_daterange(
            commissionable_invoice_items)

        self.salesperson_stats_list = CommissionSales.create_salesperson_stats(
            filtered_commissionable_invoice_items)

        self.commission_orders_list = self.generate_commission_orders(
            self.salesperson_stats_list, post_date)

        if not trial:
            self.create_spire_sales_orders(self.commission_orders_list)

        CommissionSales.write_results_to_output_csv(
            self.commission_orders_list)

        return CommissionSales.check_results(self.commission_orders_list, trial)

    def get_commission_rates(self):
        product_code_filter = {"$or": []}

        for code in SUBSCRIPTION_PRODUCT_CODE:
            product_code_filter['$or'].append({"code": code})

        for code in HOSTING_PRODUCT_CODE:
            product_code_filter['$or'].append({"code": code})

        product_code_list = self.api_client.InventoryGroups.all(
            filter=product_code_filter)

        return {code.code: (float(code.margin)/100.0) for code in product_code_list}

    # Takes a list of commissionable part numbers and gets all of the related invoice items
    def get_commissionable_invoice_items(self):
        order_filter_obj = {
            "invoiceDate": {"$gte": self.start_date.strftime('%Y-%m-%d')},
            "$or": [],
        }
        for code in SUBSCRIPTION_PRODUCT_CODE:
            order_filter_obj['$or'].append({"inventoryGroupNo": f"{code}"})

        for code in HOSTING_PRODUCT_CODE:
            order_filter_obj['$or'].append({"inventoryGroupNo": f"{code}"})

        invoice_items_list = self.api_client.SalesHistoryItems.all(
            filter=order_filter_obj)

        return invoice_items_list

    # Filters a list of invoice items to only those between the chosen start and end dates
    def filter_commissionable_invoice_items_by_daterange(self, commissionable_invoice_items):
        filtered_invoice_items = list(
            filter(
                lambda x: x.invoiceDate >= self.start_date and x.invoiceDate <= self.end_date,
                commissionable_invoice_items
            )
        )

        return filtered_invoice_items

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
                    invoice_date=invoice_item.invoiceDate,
                    salesperson_no=invoice_item.invoice.salespersonNo,
                    part_no=invoice_item.partNo,
                    part_description=invoice_item.description,
                    inventory_group_no=invoice_item.inventoryGroupNo,
                    customer_no=invoice_item.invoice.customer.customerNo,
                    customer_name=invoice_item.invoice.customer.name,
                    currency=invoice_item.invoice.currency,
                    quantity=invoice_item.committedQty,
                    amount=invoice_item.unitPrice
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
        commission_rates = self.get_commission_rates()

        spire_commission_orders = []

        for salesperson in salesperson_stats_list:
            new_sales_order = {}
            new_sales_order['customer'] = {}
            new_sales_order['customer']['customerNo'] = salesperson.salesperson_no
            new_sales_order['orderDate'] = post_date.strftime('%Y-%m-%d')
            new_sales_order['invoiceDate'] = post_date.strftime('%Y-%m-%d')
            new_sales_order['referenceNo'] = 'Commission'
            new_sales_order['items'] = []

            for invoice in salesperson.invoices:
                for item in invoice.lines:

                    date_str = item.invoice_date.strftime('%B %y')

                    if item.hosting_sales != 0:
                        line_item = {}
                        line_item['partNo'] = 'SUBHOST'
                        line_item['orderQty'] = -1 * item.quantity
                        line_item['unitPrice'] = round(item.hosting_sales *
                                                       commission_rates[item.inventory_group_no], 2)
                        line_item[
                            'description'] = f'{item.part_description} | {date_str} | {item.customer_name}'[:80]
                        new_sales_order['items'].append(line_item)

                    if item.subscription_sales != 0:
                        line_item = {}
                        line_item['partNo'] = 'SUBCOMM'
                        line_item['orderQty'] = -1 * item.quantity
                        line_item['unitPrice'] = round(item.subscription_sales *
                                                       commission_rates[item.inventory_group_no], 2)
                        line_item[
                            'description'] = f'{item.part_description} | {date_str} | {item.customer_name}'[:80]
                        new_sales_order['items'].append(line_item)

            spire_commission_orders.append(new_sales_order)

        return spire_commission_orders

    # Create the new commission sales orders in Spire
    def create_spire_sales_orders(self, commission_orders_list):
        for order in commission_orders_list:
            self.api_client.SalesOrders.new(order)

    # Write the commission sales order details out to output.csv
    def write_results_to_output_csv(commission_orders_list):
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
                        [item['partNo'], item['orderQty'], item['unitPrice'], item['description']])
                    writer.writerow(result_row)

    # Return a message indicating what happened to the GUI
    def check_results(commission_orders_list, trial):
        if len(commission_orders_list) <= 0:
            msg = 'No items found to post commissions for'
        elif trial:
            msg = 'Commission Orders saved to output.csv'
        else:
            msg = 'Commission Sales Orders Posted Successfully'
        return msg


# Create and post commission sales orders into spire via the api_client
def create_commission_sales_orders(api_client, start_date, end_date, post_date, trial=None):
    commission_sales = CommissionSales(
        api_client, start_date=start_date, end_date=end_date)
    result = commission_sales.post_commission_sales_orders(
        post_date=post_date, trial=trial)
    return result


if __name__ == '__main__':
    create_commission_sales_orders(
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
