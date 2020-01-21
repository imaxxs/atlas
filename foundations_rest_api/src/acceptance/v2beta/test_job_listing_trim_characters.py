"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""
import numpy as np
import foundations
from foundations import set_project_name
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase
from acceptance.v2beta.jobs_tests_helper_mixin_v2 import JobsTestsHelperMixinV2
from foundations_spec import *

class TestJobListingTrimCharacters(JobsTestsHelperMixinV2, APIAcceptanceTestCaseBase, Spec):
    url = '/api/v2beta/projects/{_project_name}/job_listing'
    sorting_columns = []
    filtering_columns = []

    @classmethod
    def setUpClass(klass):
        JobsTestsHelperMixinV2.setUpClass()
        klass._set_project_name('hanna')

    @classmethod
    def tearDownClass(klass):
        from foundations_contrib.global_state import redis_connection as redis
        redis.flushall()

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import redis_connection
        redis_connection.flushall()

    def submit_job(self):
        import subprocess

        submit_result = subprocess.run(
            "python -m foundations submit --project-name hanna scheduler acceptance/v2beta/fixtures/log_int_metric log_int_metric.py",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            assert submit_result.returncode == 0
        except AssertionError:
            output = submit_result.stdout.decode() or submit_result.stderr.decode()
            self.fail(output)

    def test_get_route(self):
        self.submit_job()

        data = super(TestJobListingTrimCharacters, self).test_get_route()
        self.assertEqual(data['jobs'][0]['output_metrics'][0]['value'], '5' * 100)
