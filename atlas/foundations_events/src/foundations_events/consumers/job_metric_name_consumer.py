

class JobMetricNameConsumer(object):
    """
    Class to consume the 'stage_log_middleware' channel. 
    Passes the name of job metrics into a list based on project name. 
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
        key = 'project:{}:metrics'.format(message['project_name'])
        value = message['key']
        self._redis.sadd(key, value)
