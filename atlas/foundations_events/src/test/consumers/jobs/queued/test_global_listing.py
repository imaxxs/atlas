
import unittest
from mock import Mock

from foundations_events.consumers.jobs.queued.global_listing import GlobalListing


class TestQueuedGlobalListing(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = GlobalListing(self._redis)

    def test_adds_job_to_global_queued_listing(self):
        self._consumer.call({'project_name': 'my fancy project', 'job_id': 'my fantastic job'}, None, None)
        self._redis.sadd.assert_called_with('projects:global:jobs:queued', 'my fantastic job')

    def test_adds_job_to_project_queued_listing_different_job(self):
        self._consumer.call({'project_name': 'my fancy project', 'job_id': 'my sad job'}, None, None)
        self._redis.sadd.assert_called_with('projects:global:jobs:queued', 'my sad job')
