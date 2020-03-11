
import unittest
from mock import Mock

from foundations_events.consumers.jobs.queued.project_listing_for_queued_job import ProjectListingForQueuedJob


class TestQueuedProjectListingForQueuedJob(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = ProjectListingForQueuedJob(self._redis)

    def test_adds_job_to_project_queued_listing(self):
        self._consumer.call({'project_name': 'my fancy project', 'job_id': 'my fantastic job'}, None, None)
        self._redis.sadd.assert_called_with('project:my fancy project:jobs:queued', 'my fantastic job')

    def test_adds_job_to_project_queued_listing_different_job(self):
        self._consumer.call({'project_name': 'my fancy project', 'job_id': 'my sad job'}, None, None)
        self._redis.sadd.assert_called_with('project:my fancy project:jobs:queued', 'my sad job')

    def test_adds_job_to_project_queued_listing_different_project(self):
        self._consumer.call({'project_name': 'your sad project', 'job_id': 'my sad job'}, None, None)
        self._redis.sadd.assert_called_with('project:your sad project:jobs:queued', 'my sad job')
