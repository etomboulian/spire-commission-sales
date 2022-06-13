from .crud_mixins import Read, Create


class Company:
    def __init__(self, api_client, company_name):
        api_client.company_name = company_name
        self.api_client = api_client
        self.company_name = company_name

    @property
    def InventoryItems(self):
        class InventoryWrapper(Read):
            def __init__(self, api_client):
                super().__init__(api_client, 'inventory_items')
        obj = InventoryWrapper(self.api_client)
        return obj

    @property
    def SalesOrders(self):
        class SalesOrdersWrapper(Read, Create):
            def __init__(self, api_client):
                super().__init__(api_client, 'sales_orders')
        obj = SalesOrdersWrapper(self.api_client)
        return obj

    @property
    def SalesHistory(self):
        class SalesHistoryWrapper(Read):
            def __init__(self, api_client):
                super().__init__(api_client, 'sales_history')

        obj = SalesHistoryWrapper(self.api_client)
        return obj

    @property
    def SalesHistoryItems(self):
        class SalesHistoryItemsWrapper(Read):
            def __init__(self, api_client):
                super().__init__(api_client, 'sales_history_items')

        obj = SalesHistoryItemsWrapper(self.api_client)
        return obj

    @property
    def Salesperson(self):
        class SalespersonWrapper(Read):
            def __init__(self, api_client):
                super().__init__(api_client, 'salespeople')
        obj = SalespersonWrapper(self.api_client)
        return obj

    @property
    def Territory(self):
        class TerritoryWrapper(Read):
            def __init__(self):
                super().__init__(self.api_client, 'territory')
        obj = TerritoryWrapper(self.api_client)
        return obj
