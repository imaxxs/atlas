
class SlackNotifier(object):

    def __init__(self):
        self._slack_client = self._create_client()
    
    def send_message(self, channel, message):
        if self._check_can_send(channel):
            response = self._slack_client.api_call('chat.postMessage', channel=channel, text=message)
            return response['ok']
        return True

    @staticmethod
    def _create_client():
        from slackclient import SlackClient
        import os

        slack_token = os.environ.get('FOUNDATIONS_SLACK_TOKEN')
        if slack_token is not None:
            return SlackClient(slack_token)

    def _check_can_send(self, channel):
        return self._slack_client is not None and channel is not None