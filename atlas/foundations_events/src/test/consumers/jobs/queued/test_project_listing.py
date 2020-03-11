
import unittest
from mock import Mock

from foundations_events.consumers.jobs.queued.project_listing import ProjectListing


class TestProjectListing(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = ProjectListing(self._redis)

    def test_adds_job_to_project_running_listing(self):
        self._consumer.call({'project_name': 'my fancy project', 'job_id': 'my fantastic job'}, None, None)
        self._redis.sadd.assert_called_with('project:my fancy project:jobs:running', 'my fantastic job')

    def test_adds_job_to_project_running_listing_different_job(self):
        self._consumer.call({'project_name': 'my fancy project', 'job_id': 'my sad job'}, None, None)
        self._redis.sadd.assert_called_with('project:my fancy project:jobs:running', 'my sad job')

    def test_adds_job_to_project_running_listing_different_project(self):
        self._consumer.call({'project_name': 'your sad project', 'job_id': 'my sad job'}, None, None)
        self._redis.sadd.assert_called_with('project:your sad project:jobs:running', 'my sad job')
