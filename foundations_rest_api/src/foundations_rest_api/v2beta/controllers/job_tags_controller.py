"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource
from foundations_core_rest_api_components.response import Response
from foundations_core_rest_api_components.lazy_result import LazyResult

@api_resource('/api/v2beta/projects/<string:project_name>/job_listing/<string:job_id>/tags')
class JobTagsController(object):

    def __init__(self):
        from foundations_contrib.global_state import redis_connection
        self._redis = redis_connection

    def post(self):
        job_annotations_key = 'jobs:{}:annotations'.format(self._job_id())

        if self._is_tag_set(job_annotations_key, self._tag):
            self._logger().warning('Tag `{}` updated to `{}`'.format(self._tag, self._value))
        
        self._redis.hmset(job_annotations_key, {self._key(): self._value()})

        return Response('Jobs', LazyResult(lambda: f'Tag key: {self._key()}, value: {self._value()} created for job {self._job_id()}'))
    
    def _is_tag_set(self, job_annotations_key, tag):
        annotations = self._redis.hgetall(job_annotations_key)
        decoded_annotations = {key.decode(): value.decode() for key, value in annotations.items()}

        return tag in decoded_annotations

    def _job_id(self):
        return self.params['job_id']

    def _key(self):
        return self._tag()['key']

    def _value(self):
        return self._tag()['value']

    def _tag(self):
        return self.params['tag']
    
    def _logger(self):
        from foundations_contrib.global_state import log_manager
        return log_manager.get_logger(__name__)