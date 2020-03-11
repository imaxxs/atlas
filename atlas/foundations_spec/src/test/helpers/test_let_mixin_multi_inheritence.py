

import unittest

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import *

class TestLetMixinMultiInheritence(unittest.TestCase):

    class SpecWithLet(object):
        @let
        def thing(self):
            return 'some stuff'

    class SpecWithInheritedLet(Spec, SpecWithLet):
        pass

    def setUp(self):
        self.SpecWithInheritedLet.setUpClass()
        self.spec_with_inherited_let = self.SpecWithInheritedLet()
        self.spec_with_inherited_let.setUp()

    def tearDown(self):
        self.spec_with_inherited_let.tearDown()
        self.SpecWithInheritedLet.tearDownClass()

    def test_supports_inheritence(self):
        self.assertEqual('some stuff', self.spec_with_inherited_let.thing)
        