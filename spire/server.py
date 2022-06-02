from .api_client import ApiClient
from .crud_mixins import Read, Create
from .company import Company


class Server:

    def __init__(self, hostname, username, password, port=10880):
        self.api_client = ApiClient(hostname, username, password, port)
        self.selected_company_name = None
        self.logged_in = False

        if not self.check_login():
            raise Exception('Unable to login to Spire Server')

    def check_login(self):
        status = self.Status.get()
        if status.version:
            self.logged_in = True

        return self.logged_in

    def Company(self, company_name):
        self.selected_company_name = company_name
        return Company(self.api_client, self.selected_company_name)

    @property
    def Companies(self):
        class CompanyList(Read):
            def __init__(self, api_client):
                super().__init__(api_client, 'company_list')

        obj = CompanyList(self.api_client)
        return obj

    @property
    def Status(self):
        class Status(Read):
            def __init__(self, api_client):
                super().__init__(api_client, 'status')
        obj = Status(self.api_client)
        return obj
