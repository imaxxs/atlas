
import unittest
from mock import Mock

from foundations_events.consumers.job_metric_name_consumer import JobMetricNameConsumer


class TestJobMetricNameConsumer(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = JobMetricNameConsumer(self._redis)

    def test_call_method(self):
        self._consumer.call(
            {'project_name': 'default', 'key': 'key1', 'value': 'value1'}, None, None)
        self._redis.sadd.assert_called_with('project:default:metrics', 'key1')

    def test_call_method_different_values(self):
        self._consumer.call(
            {'project_name': 'potati', 'key': 'key78', 'value': 'value1'}, None, None)
        self._redis.sadd.assert_called_with('project:potati:metrics', 'key78')
