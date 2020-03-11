
from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import *
from foundations_spec.helpers.partial_callable_mock import PartialCallableMock

def _create_retry_test(number_of_retries):
    def _callback(self):
        self.slack_notifier.send_message.side_effect = [False] * (number_of_retries-1) + [True]
        self.notifier.send_message(self.message)
        call_count = self.slack_notifier.send_message.call_count
        self.assertEqual(call_count, number_of_retries)
    return _callback

class TestJobNotifier(Spec):
    
    @let
    def channel(self):
        return self.faker.name()
    
    @let
    def channel_two(self):
        return self.faker.name()

    @let
    def message(self):
        return self.faker.sentence()

    @let
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager
        return ConfigManager()
    
    slack_notifier = let_mock()

    @let_now
    def notifier(self):
        from foundations_events.notifiers import JobNotifier
        return JobNotifier(self.config_manager, self.slack_notifier)

    def test_sends_message_to_slack_notifier(self):
        self.slack_notifier.send_message = PartialCallableMock()
        self.notifier.send_message(self.message)
        self.slack_notifier.send_message.assert_called_with_partial(message=self.message)

    def test_sends_null_channel_if_not_defined(self):
        self.slack_notifier.send_message = PartialCallableMock()
        self.notifier.send_message(self.message)
        self.slack_notifier.send_message.assert_called_with_partial(channel=None)

    def test_uses_channel_in_config(self):
        self.config_manager['job_notification_channel'] = self.channel
        self.slack_notifier.send_message = PartialCallableMock()
        self.notifier.send_message(self.message)
        self.slack_notifier.send_message.assert_called_with_partial(channel=self.channel)

    def test_sends_message_to_slack_notifier_when_first_attempt_fails(self):
        self.slack_notifier.send_message = PartialCallableMock()
        self.slack_notifier.send_message.return_value = False
        self.notifier.send_message(self.message)
        self.slack_notifier.send_message.assert_called_with_partial(message=self.message)

    def test_uses_channel_in_config(self):
        self.config_manager['job_notification_channel'] = self.channel
        self.slack_notifier.send_message = PartialCallableMock()
        self.slack_notifier.send_message.return_value = False
        self.notifier.send_message(self.message)
        self.slack_notifier.send_message.assert_called_with_partial(channel=self.channel)

    test_that_notifier_retries_after_one_failure = _create_retry_test(2)

    def test_that_notifier_does_not_retry_if_succeeds(self):
        self.slack_notifier.send_message.return_value = True
        self.notifier.send_message(self.message)
        call_count = self.slack_notifier.send_message.call_count
        self.assertEqual(call_count, 1)

    test_that_notifier_retries_three_times_after_two_failures = _create_retry_test(3)

    test_that_notifier_retries_four_times_after_three_failures = _create_retry_test(4)

    test_that_notifier_retries_five_time_after_four_failures = _create_retry_test(5)

        
        
        