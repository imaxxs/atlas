
from foundations_spec import *

class TestProjectsController(Spec):

    def test_projects_controller_comes_from_core_rest_api_components_module(self):
        import foundations_rest_api.v2beta.controllers.projects_controller as atlas
        import foundations_core_rest_api_components.v1.controllers.projects_controller as core
        self.assertEqual(core.ProjectsController, atlas.ProjectsController)

    def test_projects_controller_registered_as_api_resource(self):
        import importlib
        import foundations_core_rest_api_components.v1.controllers.projects_controller as core
        import foundations_rest_api.v2beta.controllers.projects_controller as atlas

        mock_api_resource = self.patch('foundations_core_rest_api_components.utils.api_resource.api_resource', ConditionalReturn())
        class_decorator = ConditionalReturn()
        decorated_class = Mock()

        mock_api_resource.return_when(class_decorator, '/api/v2beta/projects')
        class_decorator.return_when(decorated_class, core.ProjectsController)

        importlib.reload(atlas)

        self.assertEqual(decorated_class, atlas.ProjectsController)