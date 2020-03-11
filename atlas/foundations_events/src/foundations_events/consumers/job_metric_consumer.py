

class JobMetricConsumer(object):
    """
    Class to consume the 'stage_log_middleware' channel. 
    Passes the metric and value to a Redis list based on job_id
    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """

    def __init__(self, redis):
        self._redis = redis

    def call(self, message, timestamp, meta_data):
        """
        Adds metric names to redis list

        Arguments:
            message {dict} -- Event attributes
            timestamp {int} -- The time the event was created
            meta_data {dict} -- Additional data about the event
        """
        from foundations_internal.fast_serializer import serialize

        job_id = message['job_id']
        key = 'jobs:{}:metrics'.format(job_id)
        metric_key = message['key']
        metric_value = message['value']
        value = (timestamp, metric_key, metric_value)
        self._redis.rpush(key, serialize(value))
