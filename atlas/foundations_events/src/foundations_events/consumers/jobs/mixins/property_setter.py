
class PropertySetter(object):
    """Saves an arbitrary value as defined by the return value 
    of a function to a value in redis
    
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

        listing_name = self._listing_name()
        listing_value = self._listing_value(message)
        property_key = self._property_name()
        property_value = self._property_value(message, timestamp, meta_data)
        self._redis.set('{}:{}:{}'.format(listing_name, listing_value, property_key), property_value)

    def _listing_name(self):
        raise NotImplementedError

    def _listing_value(self, message):
        raise NotImplementedError

    def _property_name(self):
        raise NotImplementedError

    def _property_value(self, message, timestamp, meta_data):
        raise NotImplementedError
