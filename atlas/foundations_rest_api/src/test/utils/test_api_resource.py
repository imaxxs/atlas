
from mock import patch
from foundations_rest_api.utils.api_resource import api_resource
from test.helpers.api_resource_mocks import APIResourceMocks
from foundations_core_rest_api_components.lazy_result import LazyResult
from foundations_core_rest_api_components.response import Response

from foundations_spec import *

class TestAPIResource(Spec):

    @let
    def random_cookie(self):
        return {self.random_cookie_key: self.random_cookie_value}

    @let
    def cookie_string(self):
        return '{}={}'.format(self.random_cookie_key, self.random_cookie_value)

    @let
    def cookie_header(self):
        return {'Cookie': 'auth_token={}'.format(self.random_cookie_value)}

    @let
    def uri_path(self):
        return '/' + self.faker.uri_path(10)

    @let
    def random_cookie_key(self):
        return self.faker.name()

    @let
    def random_cookie_value(self):
        return self.faker.sha256()

    @let
    def random_data(self):
        return {self.faker.sentence(): self.faker.sentence() for _ in range(self.faker.random.randint(3, 10))}

    def test_returns_class(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.Mock)
        self.assertEqual(klass, APIResourceMocks.Mock)

    def test_get_returns_index(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(self._json_response(response), 'some data')
    
    def test_get_returns_show(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithShow)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(self._json_response(response), 'some specific data')

    def test_delete_returns_delete(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithDelete)
        with self._test_client() as client:
            response = client.delete(self.uri_path)
            self.assertEqual(self._json_response(response), 'some data')
        
    def test_delete_sets_params(self):
        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('delete', _callback)

        klass = api_resource(self.uri_path)(mock_klass)
        with self._test_client() as client:
            response = client.delete(self.uri_path, data=self.random_data)
            self.assertEqual(self._json_response(response), self.random_data)

    def test_post_returns_post(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithPost)
        with self._test_client() as client:
            response = client.post(self.uri_path)
            self.assertEqual(self._json_response(response), 'some data')
        
    def test_put_returns_update(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithUpdate)
        with self._test_client() as client:
            response = client.put(self.uri_path)
            self.assertEqual(self._json_response(response), 'some updated data')
    
    def test_post_sets_params(self):
        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback)

        klass = api_resource(self.uri_path)(mock_klass)
        with self._test_client() as client:
            response = client.post(self.uri_path, data={'password': 'world'})
            self.assertEqual(self._json_response(response), {'password': 'world'})

    def test_post_sets_json(self):
        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback)

        klass = api_resource(self.uri_path)(mock_klass)
        with self._test_client() as client:
            response = client.post(self.uri_path, json={'password': 'world'})
            self.assertEqual(self._json_response(response), {'password': 'world'})

    def test_post_sets_params_different_params(self):
        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback)

        klass = api_resource(self.uri_path)(mock_klass)
        with self._test_client() as client:
            response = client.post(self.uri_path, data={'password': 'world', 'cat': 'dog'})
            self.assertEqual(self._json_response(response), {'password': 'world', 'cat': 'dog'})

    def test_get_returns_index_different_data(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.DifferentMockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(self._json_response(response), 'some different data')
    
    def test_get_and_post_returns_index_and_post(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithIndexAndPost)
        with self._test_client() as client:
            post_response = client.post(self.uri_path)
            get_response = client.get(self.uri_path)
            self.assertEqual(self._json_response(post_response), 'some post data')
            self.assertEqual(self._json_response(get_response), 'some index data')

    def test_get_returns_empty_params(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(self._json_response(response), {})

    def test_get_has_status_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(response.status_code, 200)

    def test_get_has_status_code_different_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndexAndStatus)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(response.status_code, 403)

    def test_delete_has_status_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithDelete)
        with self._test_client() as client:
            response = client.delete(self.uri_path)
            self.assertEqual(response.status_code, 200)

    def test_delete_has_status_code_different_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithDeleteAndStatus)
        with self._test_client() as client:
            response = client.delete(self.uri_path)
            self.assertEqual(response.status_code, 403)

    def test_post_has_status_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithIndexAndPost)
        with self._test_client() as client:
            response = client.post(self.uri_path)
            self.assertEqual(response.status_code, 200)

    def test_post_has_status_code_different_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithPostAndStatus)
        with self._test_client() as client:
            response = client.post(self.uri_path)
            self.assertEqual(response.status_code, 403)

    def test_post_has_cookie(self):
        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback, cookie=self.random_cookie, )
        klass = api_resource(self.uri_path)(mock_klass)
        with self._test_client() as client:
            response = client.post(self.uri_path, data={'password': 'world'})
            self.assertEqual(self.cookie_string + ';path=/', response.headers.get('Set-Cookie'))

    def test_delete_returns_path_param(self):
        klass = api_resource('/path/to/resource/with/<string:project_name>/params')(APIResourceMocks.ParamsMockWithDelete)
        with self._test_client() as client:
            response = client.delete('/path/to/resource/with/value/params')
            self.assertEqual(self._json_response(response), {'project_name': 'value'})

    def test_get_returns_path_param(self):
        klass = api_resource('/path/to/resource/with/<string:project_name>/params')(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get('/path/to/resource/with/value/params')
            self.assertEqual(self._json_response(response), {'project_name': 'value'})

    def test_post_returns_path_param(self):
        klass = api_resource('/path/to/resource/with/<string:project_name>/params')(APIResourceMocks.ParamsMockWithPost)
        with self._test_client() as client:
            response = client.post('/path/to/resource/with/value/params')
            self.assertEqual(self._json_response(response), {'project_name': 'value'})

    def test_get_returns_path_with_query_params(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path + '?hello=world')
            self.assertEqual(self._json_response(response), {'hello': 'world'})

    def test_get_returns_path_with_query_list_params(self):
        klass = api_resource('/path/to/resource/with/query_list/params')(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get('/path/to/resource/with/query_list/params?hello=world&hello=lou')
            self.assertEqual(self._json_response(response), {'hello': ['world', 'lou']})


    def _empty_callback(self, mock_instance):
        return ''

    def _test_client(self):
        from foundations_rest_api.global_state import app_manager
        return app_manager.app().test_client()

    def _mock_resource(self, method, callback, status=200, cookie=None):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        mock_klass = Mock()
        mock_instance = Mock()
        mock_klass.return_value = mock_instance
        result = LazyResult(lambda: callback(mock_instance))
        getattr(mock_instance, method).side_effect = lambda: Response('Mock', result, status=status, cookie=cookie)
        return mock_klass

    def _json_response(self, response):
        from foundations.utils import string_from_bytes
        from json import loads, dumps

        data = string_from_bytes(response.data)

        return loads(data)