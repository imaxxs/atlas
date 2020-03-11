
from flask import request, make_response, Response
class APIResourceBuilder(object):

    def __init__(self, app_manager, klass, base_path):
        self._app_manager = app_manager
        self._klass = klass
        self._base_path = base_path
        self._api_actions = {}

    def _load_index_route(self):
        if hasattr(self._klass, 'index'):
            self._api_actions['get'] = self._get_api_index()
    
    def _load_post_route(self):
        if hasattr(self._klass, 'post'):
            self._api_actions['post'] = self._post_api_create()
    
    def _load_delete_route(self):
        if hasattr(self._klass, 'delete'):
            self._api_actions['delete'] = self._delete_api_create()

    def _load_put_route(self):
        if hasattr(self._klass, 'put'):
            self._api_actions['put'] = self._put_api_create()

    def _load_patch_route(self):
        if hasattr(self._klass, 'patch'):
            self._api_actions['patch'] = self._patch_api_create()
    
    def _create_action(self):
        self._load_index_route()
        self._load_post_route()
        self._load_delete_route()
        self._load_put_route()
        self._load_patch_route()
        resource_class = self._create_api_resource()
        self._add_resource(resource_class)

    def _add_resource(self, resource_class):
        self._app_manager.api().add_resource(resource_class, self._base_path)

    def _create_api_resource(self):
        from flask_restful import Resource
        import random

        class_name = '_%08x' % random.getrandbits(32)
        return type(class_name, (Resource,), self._api_actions)

    def _get_api_index(self):
        def _get(resource_self, **kwargs):
            instance = self._klass()
            instance.params = self._api_params(kwargs)

            response = instance.index()
            return response.as_json(), response.status()
            
        return _get
    
    def _post_api_create(self):
        def _post(resource_self, **kwargs):
            instance = self._klass()
            instance.params = self._api_params(kwargs)

            response = instance.post()
            cookie = None
            if response.cookie():
                cookie_key, cookie_value = list(response.cookie().items())[0]
                cookie = '{}={};path=/'.format(cookie_key, cookie_value)
            return response.as_json(), response.status(), {'Set-Cookie': cookie }
        return _post

    def _delete_api_create(self):
        def _delete(resource_self, **kwargs):
            instance = self._klass()
            instance.params = self._api_params(kwargs)

            response = instance.delete()
            return response.as_json(), response.status()
        return _delete

    def _put_api_create(self):
        def _put(resource_self, **kwargs):
            instance = self._klass()
            instance.params = self._api_params(kwargs)

            response = instance.put()
            return response.as_json(), response.status()
        return _put

    def _patch_api_create(self):
        def _patch(resource_self, **kwargs):
            instance = self._klass()
            instance.params = self._api_params(kwargs)

            response = instance.patch()
            return response.as_json(), response.status()
        return _patch

    def _api_params(self, kwargs):
        from flask import request

        params = dict(kwargs)
        dict_args = request.args.to_dict(flat=False)
        for key, value in dict_args.items():
            params[key] = value if len(value) > 1 else value[0]
        params.update(request.form)
        if request.json:
            params.update(request.json)
        return params

def api_resource(base_path):
    def _make_api_resource(klass):
        """Decorator for defining resource for controllers
        """
        from foundations_core_rest_api_components.global_state import app_manager

        APIResourceBuilder(app_manager, klass, base_path)._create_action()
        return klass

    return _make_api_resource