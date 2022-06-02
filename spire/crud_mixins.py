
class CRUDBase:
    def __init__(self, api_client, function_name):
        self.api_client = api_client
        self.function_name = function_name


class Read(CRUDBase):
    def get(self, id=None, **kwargs):
        data = self.api_client.get(self.function_name, id=id, **kwargs)
        return data

    def list(self):
        data = self.get()
        return data

    def all(self):
        page_size = 100
        results = []

        # Get the first page
        list = self.get(limit=page_size)
        total_records = list.count
        total_pages = (total_records//page_size) + 1

        # take all of the records into results list from the first page
        for item in list.records:
            results.append(item)

        # get all remaining pages and extract the data into results list
        for pageNumber in range(1, total_pages):
            list = self.get(start=(
                pageNumber*page_size), limit=page_size)
            for item in list.records:
                results.append(item)

        # return the results list
        return results


class Create(CRUDBase):
    def new(self, data):
        result = self.api_client.new(self.function_name, data)
        return result
