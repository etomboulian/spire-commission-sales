
from .models.root import (
    Status,
    # Company,
    CompanyList
)


from .models.company import (
    TerritoryList,
    SalespersonList,
    InvoiceItemList,
    Invoice,
    InvoiceList,
    SalesOrder,
    SalesOrderList
)


root_endpoint_data = {
    'status': {
        'endpoint': 'status',
        'single_type': Status,
        'collection_type': Status
    },
    'company_list': {
        'endpoint': 'companies/',
        'single_type': None,
        'collection_type': CompanyList
    }
}


company_endpoint_data = {
    'sales_orders': {
        'endpoint': 'sales/orders/',
        'single_type': SalesOrder,
        'collection_type': SalesOrderList
    },


    'sales_history': {
        'endpoint': 'sales/invoices/',
        'single_type': None,
        'collection_type': InvoiceList
    },

    'sales_history_items': {
        'endpoint': 'sales/invoice_items/',
        'single_type': None,
        'collection_type': InvoiceItemList
    },

    'salesperson_list': {
        'endpoint': 'salespeople/',
        'single_type': None,
        'collection_type': SalespersonList
    },

    'territory_list': {
        'endpoint': 'territories/',
        'single_type': None,
        'collection_type': TerritoryList
    }
}
