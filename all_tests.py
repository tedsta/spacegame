#!/usr/bin/env python

# import all the lovely files
import unittest
import test.path_tests

# get suites from test modules
suites = [
test.path_tests.suite(),
]

# collect suites in a TestSuite object
suite = unittest.TestSuite()
for s in suites:
    suite.addTest(s)

# run suite
unittest.TextTestRunner(verbosity=2).run(suite)
