
import unittest
from mock import Mock
from foundations_contrib.job_data_shaper import JobDataShaper


class TestJobDataShaper(unittest.TestCase):

    def test_data_reshaped_one_job(self):
        sample_data = [{
            'project_name': 'banana',
            'job_id': '132',
            'user': 'potter',
            'job_parameters': {'harry': 'potter'},
            'input_params': [{'ron': 'weasley', 'argument': {'agrhh': 'scream'}}],
            'output_metrics': [['123', 'hermione', 'granger']],
            'status': 'dead',
            'start_time': '456',
            'completed_time': '123'
        }]
        expected_data = [{
            'project_name': 'banana',
            'job_id': '132',
            'user': 'potter',
            'job_parameters': {'harry': 'potter'},
            'input_params': [{'ron': 'weasley', 'agrhh': 'scream'}],
            'output_metrics': {'hermione': 'granger'},
            'status': 'dead',
            'start_time': '456',
            'completed_time': '123'
        }]
        self.assertEqual(expected_data, JobDataShaper.shape_data(sample_data))

    def test_data_reshaped_one_job_different_data(self):
        sample_data = [{
            'job_parameters': {'harry': 'potter', 'tom': 'riddle'},
            'input_params': [{'ron': 'weasley', 'argument': {'wand': 'magical'}}, {'dudley': 'dursley', 'argument': {'donuts': 'good'}}],
            'output_metrics': [['123', 'hermione', 'granger'], ['1245', 'luna', 'lovegood']],
        }]
        expected_data = [{
            'job_parameters': {'harry': 'potter', 'tom': 'riddle'},
            'input_params': [{'ron': 'weasley', 'wand': 'magical'}, {'dudley': 'dursley', 'donuts': 'good'}],
            'output_metrics': {'hermione': 'granger', 'luna': 'lovegood'},

        }]
        self.assertEqual(expected_data, JobDataShaper.shape_data(sample_data))

    def test_data_reshaped_two_jobs_different_data(self):
        sample_data = [{
            'output_metrics': [['123', 'hermione', 'granger'], ['1245', 'luna', 'lovegood']],
            'input_params': [{'ron': 'weasley', 'argument': {'wand': 'magical'}}, {'dudley': 'dursley', 'argument': {'donuts': 'good'}}]
        },
            {
            'output_metrics': [['123', 'hermione', 'granger'], ['1245', 'moon', 'lovegood']],
            'input_params': [{'ron': 'weasley', 'argument': {'agrhh': 'scream'}}]
        }]
        expected_data = [{
            'output_metrics': {'hermione': 'granger', 'luna': 'lovegood'},
            'input_params': [{'ron': 'weasley', 'wand': 'magical'}, {'dudley': 'dursley', 'donuts': 'good'}]

        },
            {
            'output_metrics': {'hermione': 'granger', 'moon': 'lovegood'},
            'input_params': [{'ron': 'weasley', 'agrhh': 'scream'}]

        }]
        self.assertEqual(expected_data, JobDataShaper.shape_data(sample_data))
    
    def test_shape_output_metrics(self):
        sample_data = [['123', 'hermione', 'granger'], ['1245', 'moon', 'lovegood']]
        expected_data = {'hermione': 'granger', 'moon': 'lovegood'}
        self.assertEqual(expected_data, JobDataShaper.shape_output_metrics(sample_data))
    
    def test_shape_output_metrics_different_data(self):
        sample_data = [['123', 'bob', 'granger'], ['1245', 'moon', 'lovegood'], ['972', 'k', 'bye']]
        expected_data = {'bob': 'granger', 'moon': 'lovegood', 'k': 'bye'}
        self.assertEqual(expected_data, JobDataShaper.shape_output_metrics(sample_data))
