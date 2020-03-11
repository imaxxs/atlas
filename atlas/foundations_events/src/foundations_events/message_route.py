
class MessageRoute(object):
    """
    Creates a named route/channel that stores a list of listeners subscribed to the channel.

    Arguments:
        name {string} -- name of queue
    """
    
    def __init__(self, name):
        self._name = name
        self._listener = []
    
    def get_name(self):
        """
        Get the name of the route
        """
        return self._name
    
    def add_listener(self, listener):
        """
        Add another listener (subscriber) to the route

        Arguments:
            listener {MessageRouteListener} -- object to subscribe to route
        """
        self._listener.append(listener)

    def push_message(self, message, timestamp, metadata):
        """
        Adds a timestamp {float} and pushes a message and metadata to all the listeners in the route

        Arguments:
            message {dictionary of json seriablizable data} -- message to send to listeners
            timestamp {float} -- time the message was submitted
            metadata {dictionary of json seriablizable data}
        """
        for listener in self._listener:
            listener.call(message, timestamp, metadata)
        