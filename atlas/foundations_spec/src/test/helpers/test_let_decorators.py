
import unittest
from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import let_patch_mock_with_conditional_return
from foundations_spec.helpers.conditional_return import ConditionalReturn

class TestLetDecorators(unittest.TestCase):

    class MockSpec(Spec):
        pass

    def setUp(self):
        self._spec = self.MockSpec()
        self._spec.setUpClass()
        self._spec.setUp()

    def tearDown(self):
        self._spec.tearDown()
        self._spec.tearDownClass()

    def test_let_patch_mock_with_conditional_return_returns_conditional_return(self):
        mock = let_patch_mock_with_conditional_return('math.sqrt').evaluate(self._spec)
        self.assertIsInstance(mock, ConditionalReturn)

    def test_let_patch_mock_with_conditional_return_patches_function(self):
        import math

        mock = let_patch_mock_with_conditional_return('math.sqrt').evaluate(self._spec)
        mock.return_when(5, 5)
        self.assertEqual(5, math.sqrt(5))
    
    def test_let_patch_mock_with_conditional_return_patches_different_function(self):
        import os

        mock = let_patch_mock_with_conditional_return('os.environ').evaluate(self._spec)
        mock.return_when('hello', 'byebye')
        self.assertEqual('hello', os.environ('byebye'))