import unittest

def create_test_suite(module_dir_name):
    loader = unittest.TestLoader()
    return loader.discover(module_dir_name + '/tests', pattern='test_*.py')

def run_tests_from(module_dir_name):
    runner = unittest.TextTestRunner()
    runner.run(create_test_suite(module_dir_name))

if __name__ == '__main__':
    run_tests_from('vcat_sdk')
    run_tests_from('gcp_utils')
    run_tests_from('ssh_utils')