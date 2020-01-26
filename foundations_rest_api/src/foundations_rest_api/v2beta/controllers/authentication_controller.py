"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_core_rest_api_components.v1.controllers.authentication_controller import AuthenticationController

from foundations_core_rest_api_components.global_state import app_manager
app_manager.api().add_resource(AuthenticationController, "/api/v2beta/auth/<string:action>")