
import unittest
from mock import patch

from foundations_core_rest_api_components.v1.controllers.projects_controller import ProjectsController

class TestProjectsController(unittest.TestCase):

    @patch('foundations_core_rest_api_components.v1.models.project.Project.all')
    def test_index_returns_all_projects(self, mock):
        mock.return_value = self._make_lazy_result('snowbork drones')

        controller = ProjectsController()

        expected_result = [{'name': 'snowbork drones', 'created_at': None, 'owner': None}]
        self.assertEqual(expected_result, controller.index().as_json())

    @patch('foundations_core_rest_api_components.v1.models.project.Project.all')
    def test_index_returns_all_projects_different_projects(self, mock):
        mock.return_value = self._make_lazy_result('space2vec')

        controller = ProjectsController()

        expected_result = [{'name': 'space2vec', 'created_at': None, 'owner': None}]
        self.assertEqual(expected_result, controller.index().as_json())

    def _make_lazy_result(self, name):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        from foundations_core_rest_api_components.v1.models.project import Project

        def _callback():
            return [Project(name=name)]

        return LazyResult(_callback)
