
class JobEventNotifier(object):
    """Sends a notification message when a job has entered a new state
    
    Arguments:
        job_notifier {JobNofitier} -- A JobNotifier for sending out the messages
    """
    
    def __init__(self, job_notifier):
        self._job_notifier = job_notifier

    def call(self, message, timestamp, meta_data):
        """See above
        
        Arguments:
            message {dict} -- Event attributes
            timestamp {int} -- The time the event was created
            meta_data {dict} -- Additional data about the event
        """

        self._job_notifier.send_message(
            """
Job {}
Job Id: {}
Timestamp: {}
Project Name: {}
            """.format(self._state(), message['job_id'], self._readable_timestamp(timestamp), message['project_name'])
        )

    @staticmethod
    def _state():
        pass

    @staticmethod
    def _readable_timestamp(timestamp):
        from datetime import datetime
        return datetime.fromtimestamp(timestamp)
    