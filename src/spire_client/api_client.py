import requests
import urllib.parse
import json
from .endpoints import root_endpoint_data, company_endpoint_data


class ApiClient:
    version = '0.0.1'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': f'Spire API Client v{version}'
    }

    proxies = {'http': 'http://127.0.0.1:8080'}

    def __init__(self, hostname, username, password, port):
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update(self.headers)
        self._company_name = None

        self.base_url = f'http://{hostname}:{port}/api/v2/'

    @property
    def company_name(self):
        return self._company_name

    @company_name.setter
    def company_name(self, value):
        self._company_name = value

    def _check_response(request_type, response):
        # for GET requests we expect a 200 response
        if request_type == 'GET':
            if response.status_code != 200:
                raise Exception(f'{response.status_code}, {response.text}')
        # for POST requests we expect a 201 response
        elif request_type == 'POST':
            if response.status_code != 201:
                raise Exception(f'{response.status_code}, {response.text}')
        # for DELETE requests we expect a 204 response
        elif request_type == 'DELETE':
            if response.status_code != 204:
                raise Exception(f'{response.status_code}, {response.text}')

    def get_selected_endpoint(self, endpoint_name):
        selected_endpoint = None

        # Figure out the url to call from the parameters passed in
        if endpoint_name in root_endpoint_data:
            selected_endpoint = root_endpoint_data[endpoint_name]
            url = self.base_url + \
                selected_endpoint['endpoint']

        elif endpoint_name in company_endpoint_data:
            if not self.company_name:
                raise Exception(
                    'Unable to call a company endpoint without a company set')
            selected_endpoint = company_endpoint_data[endpoint_name]
            url = self.base_url + 'companies/' + self.company_name + \
                '/' + selected_endpoint['endpoint']

        else:
            raise Exception(
                f'Unable to determine endpoint from the given data, endpoint:{selected_endpoint} id:{id}')

        selected_endpoint['url'] = url
        return selected_endpoint

    @classmethod
    def deserialize(cls, response, is_single_type, selected_endpoint):
        obj = None
        if is_single_type:
            obj_type = selected_endpoint['single_type']
        else:
            obj_type = selected_endpoint['collection_type']

        if obj_type:
            obj = obj_type(**response)
        else:
            raise Exception(
                f'Unable to deserialize result of API Call: obj_type: {obj_type}, selected_endpoint: {selected_endpoint}')

        return obj

    def get(self, endpoint_name, id=None, **kwargs):
        # Get selected endpoint data and get the URL from it
        selected_endpoint = self.get_selected_endpoint(endpoint_name)

        is_single_record_type = True if id else False

        if is_single_record_type:
            url += id

        def populate_params():
            params = {}

            # Account for pagination parameters (start, limit) passed in as kwargs
            if kwargs.get('start'):
                params['start'] = kwargs.get('start')
            if kwargs.get('limit'):
                params['limit'] = kwargs.get('limit')

            # Get and send filter into params if it was passed in as kwarg
            filter = kwargs.get('filter', None)
            if filter:
                params['filter'] = json.dumps(filter)

            # Set proxies if proxy was passed in as kwarg
            if kwargs.get('proxy'):
                proxies = kwargs.get('proxy')

            return params
        proxies = {'http': 'http://127.0.0.1:8080'}
        # Do get request
        try:
            response = self.session.get(
                selected_endpoint['url'],
                params=populate_params(),
                proxies=proxies
            )

            self.__class__._check_response('GET', response)
            response = response.json()
            obj = self.deserialize(
                response, is_single_record_type, selected_endpoint)
            return obj

        except Exception as e:
            raise e

    def new(self, endpoint_name, data):
        selected_endpoint = self.get_selected_endpoint(endpoint_name)

        try:
            first_response = self.session.post(
                selected_endpoint['url'], json=data)
            header_text = 'Headers: {}'.format(first_response.headers)
            response_code = 'Response Code: {}'.format(
                first_response.status_code)
            text = 'Text: {}'.format(first_response.text)
        except:
            raise Exception("\n".join([header_text, response_code, text]))

        self.__class__._check_response('POST', first_response)

        created_item_endpoint = first_response.headers.get('Location')

        if created_item_endpoint:
            second_response = self.session.get(created_item_endpoint)
            self.__class__._check_response('GET', second_response)
            second_response = second_response.json()

            obj = self.deserialize(second_response, True, selected_endpoint)
            return obj
        else:
            raise Exception('Unable to get the created resource')
