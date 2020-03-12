from acceptance.v2beta.jobs_tests_helper_mixin_v2 import JobsTestsHelperMixinV2
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase


class TestJobsListingEndpointV2(JobsTestsHelperMixinV2, APIAcceptanceTestCaseBase):
    url = '/api/v2beta/projects/{_project_name}/job_listing'
    sorting_columns = ['start_time', 'status']
    filtering_columns = [
        {
            'name': 'job_id',
            'test_values': ('00000000-0000-0000-0000-000000000000', 'my job 1')
        },
        {
            'name': 'status',
            'test_values': ('queued', 'running')
        },
        {
            'name': 'user',
            'test_values': ('beethoven', 'soju hero')
        },
        {
            'name': 'duration',
            'test_values': ('1_0_0_0', '2_0_0_0')
        },
        {
            'name': 'start_time',
            'test_values': ('03_03_1973_09_46', '11_29_1973_21_33')
        }
    ]

    running_tags = {
        'am_i_running': 'True',
        'num_gpus': 20
    }

    completed_tags = {
        'am_i_running': 'False',
        'num_gpus': 0,
        'cool': 'dude'
    }

    expected_running_tags = {
        'am_i_running': 'True',
        'num_gpus': '20'
    }

    expected_completed_tags = {
        'am_i_running': 'False',
        'num_gpus': '0',
        'cool': 'dude'
    }

    @classmethod
    def setUpClass(klass):
        JobsTestsHelperMixinV2.setUpClass()
        klass._set_project_name(JobsTestsHelperMixinV2._str_random_uuid())
        klass._setup_five_jobs()

    @classmethod
    def _setup_five_jobs(klass):
        klass._make_running_job('00000000-0000-0000-0000-000000000000', 'soju hero', start_timestamp=99999999, tags=klass.running_tags)
        klass._make_completed_job('my job 1', 'beethoven', start_timestamp=100000000, end_timestamp=100086400)
        klass._make_completed_job('my job 2', 'mozart', start_timestamp=123456780, end_timestamp=123555555, tags=klass.completed_tags)
        klass._make_queued_job('queued job 0', 'kyle')
        klass._make_queued_job('queued job 1', 'jinnah')

    def test_get_route(self):
        data = super(TestJobsListingEndpointV2, self).test_get_route()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][3]['job_id'], 'queued job 1')
        self.assertEqual(data['jobs'][4]['job_id'], 'queued job 0')

    def test_get_tags(self):
        data = super(TestJobsListingEndpointV2, self).test_get_route()
        self.assertEqual(data['jobs'][0]['tags'], self.expected_completed_tags)
        self.assertEqual(data['jobs'][1]['tags'], {})
        self.assertEqual(data['jobs'][2]['tags'], self.expected_running_tags)
        self.assertEqual(data['jobs'][3]['tags'], {})
        self.assertEqual(data['jobs'][4]['tags'], {})

    def test_duration(self):
        import re

        regex = re.compile(r'\d+d\d+h\d+m\d+s')
        data = super(TestJobsListingEndpointV2, self).test_get_route()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertIsNotNone(regex.match(data['jobs'][0]['duration']))
        self.assertEqual(data['jobs'][4]['job_id'], 'queued job 0')
        self.assertIsNone(data['jobs'][4]['duration'])


    def test_sorted_start_time_descending(self):
        data = super(TestJobsListingEndpointV2, self).test_sorted_start_time_descending()
        self.assertEqual(data['jobs'][0]['job_id'], 'queued job 1')
        self.assertEqual(data['jobs'][1]['job_id'], 'queued job 0')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][3]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][4]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_sorted_start_time_ascending(self):
        data = super(TestJobsListingEndpointV2, self).test_sorted_start_time_ascending()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')

    def test_sorted_status_descending(self):
        data = super(TestJobsListingEndpointV2, self).test_sorted_status_descending()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'queued job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'queued job 0')
        self.assertEqual(data['jobs'][3]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][4]['job_id'], 'my job 1')

    def test_sorted_status_ascending(self):
        data = super(TestJobsListingEndpointV2, self).test_sorted_status_ascending()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'queued job 1')
        self.assertEqual(data['jobs'][3]['job_id'], 'queued job 0')
        self.assertEqual(data['jobs'][4]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_all_ascending(self):
        data = super(TestJobsListingEndpointV2, self).test_all_ascending()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][3]['job_id'], 'queued job 0')
        self.assertEqual(data['jobs'][4]['job_id'], 'queued job 1')

    def test_all_descending(self):
        data = super(TestJobsListingEndpointV2, self).test_all_descending()
        self.assertEqual(data['jobs'][0]['job_id'], 'queued job 1')
        self.assertEqual(data['jobs'][1]['job_id'], 'queued job 0')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][3]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][4]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_alternation(self):
        data = super(TestJobsListingEndpointV2, self).test_alternation()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')

    def test_filter_job_id_range(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_job_id_range()
        self.assertEqual(len(data['jobs']), 2)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_job_id_exact_match_one_option(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_job_id_exact_match_one_option()
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_job_id_exact_match_two_options(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_job_id_exact_match_two_options()
        self.assertEqual(len(data['jobs']), 2)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_status_range(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_status_range()
        self.assertEqual(len(data['jobs']), 3)
        self.assertEqual(data['jobs'][2]['job_id'], 'queued job 0')

    def test_filter_status_exact_match_one_option(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_status_exact_match_one_option()
        self.assertEqual(len(data['jobs']), 2)

    def test_filter_status_exact_match_two_options(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_status_exact_match_two_options()
        self.assertEqual(len(data['jobs']), 3)
        self.assertEqual(data['jobs'][2]['job_id'], 'queued job 0')

    def test_filter_user_range(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_user_range()
        self.assertEqual(len(data['jobs']), 5)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][3]['job_id'], 'queued job 1')
        self.assertEqual(data['jobs'][4]['job_id'], 'queued job 0')

    def test_filter_user_exact_match_one_option(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_user_exact_match_one_option()
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')

    def test_filter_user_exact_match_two_options(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_user_exact_match_two_options()
        self.assertEqual(len(data['jobs']), 2)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_job_id_contains(self):
        custom_test_method = super(TestJobsListingEndpointV2, self)._get_test_route_method('?job_id_contains=1')
        data = custom_test_method(self)
        self.assertEqual(len(data['jobs']), 2)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')

    def test_filter_user_contains(self):
        custom_test_method = super(TestJobsListingEndpointV2, self)._get_test_route_method('?user_contains=hero')
        data = custom_test_method(self)
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_duration_range(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_duration_range()
        self.assertEqual(len(data['jobs']), 2)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')

    def test_filter_duration_exact_match_one_option(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_duration_exact_match_one_option()
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')

    def test_filter_duration_exact_match_two_options(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_duration_exact_match_two_options()
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')

    def test_filter_start_time_range(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_start_time_range()
        self.assertEqual(len(data['jobs']), 3)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_start_time_exact_match_one_option(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_start_time_exact_match_one_option()
        self.assertEqual(len(data['jobs']), 0)

    def test_filter_start_time_exact_match_two_options(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_start_time_exact_match_two_options()
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
