
class ProjectTracker(object):
    """
    
    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """
    
    def __init__(self, redis):
        self._redis = redis

    def call(self, message, timestamp, meta_data):
        """See above
        
        Arguments:
            message {dict} -- Event attributes
            timestamp {int} -- The time the event was created
            meta_data {dict} -- Additional data about the event
        """

        project_name = message['project_name']
        self._redis.execute_command('ZADD', 'projects', 'NX', timestamp, project_name)
