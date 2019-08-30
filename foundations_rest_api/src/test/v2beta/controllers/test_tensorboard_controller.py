"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
import os
from random import randint

import unittest
from mock import patch

from foundations.artifacts.syncable_directory import SyncableDirectory
from foundations_rest_api.v2beta.controllers.tensorboard_controller import TensorboardController
from foundations_rest_api.v2beta.models.property_model import PropertyModel
from foundations_spec import *

class TestTensorboardController(Spec):

    mock_request_post = let_patch_mock('requests.post')

    @let_now
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager

        config_manager = ConfigManager()
        config_manager['TENSORBOARD_API_HOST'] = self.api_host_name
        config_manager['TENSORBOARD_HOST'] = self.host_name
        return self.patch('foundations_contrib.global_state.config_manager', config_manager)

    @let
    def api_host_name(self):
        return f'http://{self.faker.word()}:32766'

    @let
    def host_name(self):
        return f'http://{self.faker.word()}:32767'

    @let
    def controller(self):
        return TensorboardController()
    
    @let
    def job_id(self):
        return [self.faker.uuid4()]

    @let
    def params(self):
        return {'tensorboard_locations': [{'job_id': self.job_id, 'synced_directory': 'tb_data'}]}

    @set_up
    def set_up(self):
        self.controller.params = self.params

    def test_tensorboard_controller_post_posts_to_the_tensorboard_api_server_with_given_params(self):
        self.controller.post()
        self.mock_request_post.assert_called_with(f'{self.api_host_name}/create_sym_links', json=self.params)

    def test_tensorboard_controller_post(self):
        self.controller.post()
        self.assertEqual({'url': f'{self.host_name}'}, self.controller.post().as_json())
 
        