
import unittest
import gcp_utils_fixtures.gcp_job_deployment_fixtures as gcf
import foundations.constants as constants

class TestGCPJobDeployment(unittest.TestCase):
    def test_job_never_finishes(self):
        never_done = gcf.NeverFinishDeployment()

        self.assertEqual(constants.deployment_running, never_done.get_job_status())
        
    def test_job_completed_instantly(self):
        done = gcf.SuccessfulMockDeployment()

        self.assertEqual(constants.deployment_completed, done.get_job_status())

    def test_job_failed_instantly(self):
        failed = gcf.FailedMockDeployment()

        self.assertEqual(constants.deployment_error, failed.get_job_status())

    def test_takes_one_second(self):
        deploy = gcf.TakesOneSecond()

        for _ in range(0, 1):
            self.assertEqual(constants.deployment_running, deploy.get_job_status())

        self.assertEqual(constants.deployment_completed, deploy.get_job_status())
        self.assertEqual(constants.deployment_completed, deploy.get_job_status())

    def test_takes_two_seconds(self):
        deploy = gcf.TakesTwoSeconds()

        for _ in range(0, 2):
            self.assertEqual(constants.deployment_running, deploy.get_job_status())

        self.assertEqual(constants.deployment_completed, deploy.get_job_status())
        self.assertEqual(constants.deployment_completed, deploy.get_job_status())

    def test_takes_random_time(self):
        deploy = gcf.SuccessfulTakesRandomTime()

        while deploy.get_job_status() == constants.deployment_running:
            pass

        self.assertEqual(constants.deployment_completed, deploy.get_job_status())
        self.assertEqual(constants.deployment_completed, deploy.get_job_status())

    def test_fails_random_time(self):
        deploy = gcf.FailedTakesRandomTime()

        while deploy.get_job_status() == constants.deployment_running:
            pass

        self.assertEqual(constants.deployment_error, deploy.get_job_status())
        self.assertEqual(constants.deployment_error, deploy.get_job_status())