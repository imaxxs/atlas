"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations_rest_api.utils.api_resource import api_resource


class TestAPIResource(unittest.TestCase):
    class Mock(object):
        pass

    class MockWithIndex(object):
        def index(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _index():
                return 'some data'
            return Response('Mock', LazyResult(_index))
    
    class MockWithPost(object):
        def post(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _post():
                return 'some data'
            return Response('Mock', LazyResult(_post))
    
    class MockWithIndexAndPost(object):
        def index(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _index():
                return 'some index data'
            return Response('Mock', LazyResult(_index))
            
        def post(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _post():
                return 'some post data'
            return Response('Mock', LazyResult(_post))

    class ParamsMockWithIndex(object):
        def index(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _index():
                return self.params
            return Response('Mock', LazyResult(_index))

    class ParamsMockWithIndexAndStatus(object):
        def index(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _index():
                return self.params
            return Response('Mock', LazyResult(_index), status=403)

    class DifferentMockWithIndex(object):
        def index(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _index():
                return 'some different data'
            return Response('Mock', LazyResult(_index))

    def test_returns_class(self):
        klass = api_resource('/path/to/resource')(self.Mock)
        self.assertEqual(klass, self.Mock)

    def test_get_returns_index(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource')(self.MockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource')
            self.assertEqual(self._json_response(response), 'some data')
    
    def test_post_returns_post(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource')(self.MockWithPost)
        with app_manager.app().test_client() as client:
            response = client.post('/path/to/resource')
            self.assertEqual(self._json_response(response), 'some data')

    def test_get_returns_index_different_data(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/different/resource')(self.DifferentMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/different/resource')
            self.assertEqual(self._json_response(response), 'some different data')
    
    def test_get_and_post_returns_index_and_post(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/another/resource')(self.MockWithIndexAndPost)
        with app_manager.app().test_client() as client:
            post_response = client.post('/path/to/another/resource')
            get_response = client.get('/path/to/another/resource')
            self.assertEqual(self._json_response(post_response), 'some post data')
            self.assertEqual(self._json_response(get_response), 'some index data')

    def test_get_returns_empty_params(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/params')(self.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/params')
            self.assertEqual(self._json_response(response), {})

    def test_get_has_status_code(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/params')(self.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/params')
            self.assertEqual(response.status_code, 200)

    def test_get_has_status_code_different_code(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/params/and/status/code')(self.ParamsMockWithIndexAndStatus)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/params/and/status/code')
            self.assertEqual(response.status_code, 403)

    def test_get_returns_path_param(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/<string:project_name>/params')(self.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/value/params')
            self.assertEqual(self._json_response(response), {'project_name': 'value'})

    def test_get_returns_path_with_query_params(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/query/params')(self.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/query/params?hello=world')
            self.assertEqual(self._json_response(response), {'hello': 'world'})

    def test_get_returns_path_with_query_list_params(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/query_list/params')(self.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/query_list/params?hello=world&hello=lou')
            self.assertEqual(self._json_response(response), {'hello': ['world', 'lou']})

    def _json_response(self, response):
        from foundations.utils import string_from_bytes
        from json import loads

        data = string_from_bytes(response.data)
        return loads(data)