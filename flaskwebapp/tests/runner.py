import unittest
from flaskwebapp.tests.user_tests import *


if __name__ == '__main__':
    loader = unittest.TestLoader()
    test_classes = [RegisterTestCases, LoginTestCases]
    suites_list = []

    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
