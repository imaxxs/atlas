"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *

from foundations_production.preprocessor_class import Preprocessor

class TestPreprocessorClass(Spec):

    mock_transformer = let_mock()

    def test_preprocessor_sets_active_preprocessor_to_itself_when_called(self):
        preprocessor_instance = Preprocessor()
        preprocessor_instance()
        self.assertIs(preprocessor_instance, Preprocessor.active_preprocessor)

    def test_new_transformer_returns_transformer_index_of_0_when_first_transformer_added(self):
        preprocessor_instance = Preprocessor()
        transformer_id = preprocessor_instance.new_transformer(self.mock_transformer)
        self.assertEqual(0, transformer_id)